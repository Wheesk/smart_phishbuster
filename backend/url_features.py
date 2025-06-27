import re
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import socket
import requests
from bs4 import BeautifulSoup
import whois
import datetime
import time 
import logging

from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


FEATURE_NAMES = [
    "UsingIP", "LongURL", "ShortURL", "Symbol@", "Redirecting//",
    "PrefixSuffix-", "SubDomains", "HTTPS", "Favicon", "NonStdPort",
    "HTTPSDomainURL", "RequestURL", "AnchorURL", "LinksInScriptTags",
    "ServerFormHandler", "StatusBarCust", "DisableRightClick",
    "UsingPopupWindow", "IframeRedirection", "InfoEmail", "AbnormalURL",
    "WebsiteForwarding", "DomainRegLen", "AgeOfDomain", "DNSRecording",
    "WebsiteTraffic", "PageRank", "GoogleIndex", "LinksPointingToPage",
    "SafeBrowsing"
]
EXPECTED_FEATURE_COUNT = len(FEATURE_NAMES)

# cache WHOIS lookups so repeat calls for the same domain return instantly
@lru_cache(maxsize=512)
def cached_whois(host):
    try:
        return whois.whois(host)
    except:
        return None  

# cache Safe Browsing checks so repeat calls for the same URL return instantly
@lru_cache(maxsize=1024)
def cached_safe_browsing(url):
    return check_safe_browsing(url, API_KEY)

def fetch_external_scores(host, url):
    """
    In parallel: website traffic, backlinks, PageRank, and Safe Browsing.
    Returns a list of 5 ints in the order:
    [traffic, page_rank, google_index, backlinks, safe_browsing]
    """
    with ThreadPoolExecutor(max_workers=4) as ex:
        f1 = ex.submit(get_website_traffic_score, host)
        f2 = ex.submit(get_backlink_score, host)
        f3 = ex.submit(get_openpagerank_score, host)
        f4 = ex.submit(cached_safe_browsing, url)
        
        traffic     = f1.result(timeout=2)
        backlink    = f2.result(timeout=2)
        opr         = f3.result(timeout=2)
        safe_sb     = f4.result(timeout=2)

    
    try:
        g = requests.get(
            f"https://www.google.com/search?q=site:{host}",
            headers={"User-Agent":"Mozilla/5.0"},
            timeout=2
        )
        google_index = 1 if "did not match any documents" not in g.text else -1
    except:
        google_index = -1

    return [traffic, opr, google_index, backlink, safe_sb]

def check_safe_browsing(url, api_key):
    try:
        body = {
            "client": {"clientId": "smartphishbuster", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE","SOCIAL_ENGINEERING","UNWANTED_SOFTWARE","POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        res = requests.post(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}",
            json=body, timeout=5
        )
        return 1 if res.status_code==200 and res.json().get("matches") else -1
    except:
        return -1

def get_openpagerank_score(domain, api_key="0cgkgkowkws8wsc88oo004goo0o0oww8c00w40ss"):
    try:
        res = requests.get(
            f"https://openpagerank.com/api/v1.0/getPageRank?domains[]={domain}",
            headers={'API-OPR': api_key}, timeout=5
        )
        rank = res.json()['response'][0].get('page_rank_integer', -1)
        return 1 if rank>=3 else -1
    except:
        return -1

def get_website_traffic_score(domain):
    try:
        res = requests.get(f"https://www.google.com/search?q=site:{domain}",
                           headers={"User-Agent":"Mozilla/5.0"}, timeout=5)
        return 1 if "did not match any documents" not in res.text else -1
    except:
        return -1

def get_backlink_score(domain):
    try:
        res = requests.get(f"https://www.google.com/search?q=link:{domain}",
                           headers={"User-Agent":"Mozilla/5.0"}, timeout=5)
        return 1 if "did not match any documents" not in res.text else -1
    except:
        return -1

def extract_features_from_url(url):
    features = []
    parsed = urlparse(url)
    host = parsed.hostname or ""
    path = parsed.path or ""
    scheme = parsed.scheme

    # --- URL-based (1–11) (fast checks) ---
    features.append(1 if re.match(r'\d+\.\d+\.\d+\.\d+', host) else -1)
    features.append(1 if len(url) >= 75 else -1)
    features.append(1 if re.search(r'bit\.ly|goo\.gl|tinyurl|shorturl', url) else -1)
    features.append(1 if '@' in url else -1)
    features.append(1 if '//' in path else -1)
    features.append(1 if '-' in host else -1)
    features.append(1 if host.count('.') > 3 else -1)
    features.append(1 if scheme != 'https' else -1)
    features.append(1 if re.search(r'favicon\.', url) else -1)
    features.append(1 if parsed.port and parsed.port not in [80,443] else -1)
    features.append(1 if 'https' in host and scheme != 'https' else -1)

    # mark start of external work
    start_external = time.time()

    # --- Content-based (12–19) ---
    t_content = time.time()
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        total = same = 0
        for tag in soup.find_all(['img','audio','video','script']):
            s = tag.get('src','')
            if s.startswith('http'):
                total += 1
                if host in s:
                    same += 1
        features.append(1 if total>0 and same/total<0.5 else -1)

        anchors = soup.find_all('a')
        bad = sum(1 for a in anchors if '#' in (a.get('href') or '') or 'javascript' in (a.get('href') or ''))
        features.append(1 if anchors and bad/len(anchors)>0.5 else -1)

        features.append(1 if len(soup.find_all('script'))+len(soup.find_all('iframe'))>10 else -1)
        forms = soup.find_all('form')
        features.append(1 if any('mailto:' in (f.get('action') or '') or '//' in (f.get('action') or '') for f in forms) else -1)
        features.append(1 if "window.status" in r.text else -1)
        features.append(1 if "event.button==2" in r.text or "contextmenu" in r.text else -1)
        features.append(1 if "window.open" in r.text else -1)
        features.append(1 if '<iframe' in r.text else -1)
    except:
        features.extend([-1]*8)
    finally:
        print(f"[Timing] Content checks: {time.time() - t_content:.2f}s")

    # --- Domain/email-based (20–22) ---
    t_net = time.time()
    try:
        features.append(1 if re.search(r'[\w\.-]+@[\w\.-]+', url) else -1)
        ip = socket.gethostbyname(host)
        features.append(1 if ip not in url else -1)
        rr = requests.get(url, timeout=5, allow_redirects=True)
        features.append(1 if len(rr.history)>2 else -1)
    except:
        features.extend([-1]*3)
    finally:
        print(f"[Timing] Email/redirect checks: {time.time() - t_net:.2f}s")

    # --- Domain age/WHOIS (23–25) ---
    t_whois = time.time()
    try:
        info = whois.whois(host)
        cd = info.creation_date[0] if isinstance(info.creation_date, list) else info.creation_date
        ed = info.expiration_date[0] if isinstance(info.expiration_date, list) else info.expiration_date
        age = (datetime.datetime.now() - cd).days if cd else 0
        validity = (ed - cd).days if cd and ed else 0
        features.append(1 if validity<365 else -1)
        features.append(1 if age<180 else -1)
        features.append(1 if info.domain_name else -1)
    except:
        features.extend([-1]*3)
    finally:
        print(f"[Timing] WHOIS lookup: {time.time() - t_whois:.2f}s")
     

    external_feats = fetch_external_scores(host, url)
    features.extend(external_feats)

    # total external
    print(f"[Timing] Total external time: {time.time() - start_external:.2f}s")

    # --- Final pad/truncate to 30 ---
    if len(features) != EXPECTED_FEATURE_COUNT:
        diff = EXPECTED_FEATURE_COUNT - len(features)
        if diff > 0:
            features.extend([-1]*diff)
        else:
            features = features[:EXPECTED_FEATURE_COUNT]

    return features

