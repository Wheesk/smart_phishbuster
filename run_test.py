
import os
import sys
import traceback

project_root = os.path.dirname(os.path.abspath(__file__))

# 1) Add project root to path so 'import backend.app' works
sys.path.insert(0, project_root)
# 2) Also add backend/ itself so 'import model_loader' inside backend/app.py works
sys.path.insert(0, os.path.join(project_root, 'backend'))

# Now import your modules 
from backend.url_features import extract_features_from_url, EXPECTED_FEATURE_COUNT
from backend.app import app

#Simple assertion helper 
def check(cond, msg):
    if not cond:
        raise AssertionError(msg)

print("Testing url_features.extract_features_from_url")

# Test 1: IP-based URL
feats = extract_features_from_url("http://192.168.0.1/login")
check(isinstance(feats, list), "Should return a list")
check(len(feats) == EXPECTED_FEATURE_COUNT,
      f"Expected {EXPECTED_FEATURE_COUNT} features, got {len(feats)}")
check(feats[0] == 1, "UsingIP flag should be 1 for IP URL")

# Test 2: HTTPS flag
feats_http  = extract_features_from_url("http://example.com")
feats_https = extract_features_from_url("https://example.com")
check(feats_http[7] == 1, "HTTP (no TLS) should yield 1 at index 7")
check(feats_https[7] == -1, "HTTPS should yield -1 at index 7")

# Test 3: Graceful failure
feats_bad = extract_features_from_url("http://nonexistent.invalid")
check(isinstance(feats_bad, list), "Should still return a list")
check(len(feats_bad) == EXPECTED_FEATURE_COUNT,
      "Should still return full-length vector on failure")

print("url_features tests passed.\n")

print("Testing backend.app /predict endpoint")
client = app.test_client()

# Missing URL
resp = client.post("/predict", json={})
check(resp.status_code == 400, "Missing URL should return 400")
print("  • Missing-URL → 400 OK")

# Legit URL
resp = client.post("/predict", json={"url": "https://www.google.com"})
check(resp.status_code == 200, "Legit URL should return 200")
data = resp.get_json()
for key in ("url", "result", "phishing_probability", "threshold"):
    check(key in data, f"Response missing '{key}' field")
check(data["result"] in ("legit","phishing"), "Result should be 'legit' or 'phishing'")
print(f"  • Legit URL → 200 OK, result = {data['result']}")

# Phish-like URL
test_url = "http://192.168.0.1/login"
resp = client.post("/predict", json={"url": test_url})
check(resp.status_code == 200, "Phish URL should return 200")
data = resp.get_json()
check(data["url"] == test_url, "Response URL mismatch")
check(0.0 <= data["phishing_probability"] <= 1.0, "Probability must be between 0 and 1")
print(f"  • Phish URL → 200 OK, probability = {data['phishing_probability']}")

print("/predict endpoint tests passed.\n")
print("All manual tests passed!")
