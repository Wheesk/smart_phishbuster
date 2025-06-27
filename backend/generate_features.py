import pandas as pd
import time
import os
from url_features import extract_features_from_url

# === 1) Feature names in exact order ===
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

# === 2) Paths ===
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir   = os.path.abspath(os.path.join(script_dir, os.pardir))
data_dir   = os.path.join(root_dir, "data")

input_csv  = os.path.join(data_dir, "balanced_dataset_spaced.csv")
output_csv = os.path.join(data_dir, "full_feature_dataset.csv")

os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === 3) Load raw dataset ===
df = pd.read_csv(input_csv)

all_features = []
labels       = []
valid_count  = 0
skip_count   = 0

# === 4) Extract features row by row ===
for idx, row in df.iterrows():
    url       = row.get("url") or row.get("URL") or row.get("Url")
    raw_label = row.get("class") or row.get("Class") or row.get("Result")

    if pd.isna(url):
        print(f"[{idx+1}] ⛔ Skipped (no URL)")
        skip_count += 1
        continue

    print(f"[{idx+1}/{len(df)}] 🔍 Extracting: {url}")
    try:
        features = extract_features_from_url(url)
        if len(features) != len(FEATURE_NAMES):
            print(f"❌ Skipped: {url} → got {len(features)} features (expected {len(FEATURE_NAMES)})")
            skip_count += 1
            continue

        try:
            label = int(str(raw_label).strip())
        except:
            print(f"❌ Skipped: {url} → invalid label '{raw_label}'")
            skip_count += 1
            continue

        all_features.append(features)
        labels.append(label)
        valid_count += 1

    except Exception as e:
        print(f"⚠️ Error for {url}: {e}")
        skip_count += 1

    time.sleep(0.3)

# === 5) Build and save the full-feature CSV ===
df_out = pd.DataFrame(all_features, columns=FEATURE_NAMES)
df_out["class"] = labels
df_out.to_csv(output_csv, index=False)

print("\n✅ Done!")
print(f"Total rows   : {len(df)}")
print(f"Valid saved  : {valid_count}")
print(f"Skipped      : {skip_count}")
print(f"Output file  : {output_csv}")
