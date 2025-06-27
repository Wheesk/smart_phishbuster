# app.py
import logging
import os
from flask import Flask, request, jsonify
from model_loader import load_model_and_scaler, load_feature_names
from url_features import extract_features_from_url

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# load model & scaler
model, scaler = load_model_and_scaler()
model, scaler = load_model_and_scaler()
expected = load_feature_names()
if expected is None:
    raise RuntimeError("feature_names.txt not found in model/")

# load feature names
model, scaler = load_model_and_scaler()
expected_features = load_feature_names()
if expected_features is None:
    raise RuntimeError("❌ feature_names.txt not found in model/")
WHITELIST = ["google.com", "github.com", "stackoverflow.com", "booking.com", "kayak.com"]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify(error="No URL provided"), 400

    url = data['url']
    logger.info("Predict: %s", url)

    # whitelist
    if any(w in url for w in WHITELIST):
        logger.info("Whitelisted")
        return jsonify(
            url=url, result="legit", source="whitelist",
            phishing_probability=0.0, threshold=0.2
        )

    try:
        feats = extract_features_from_url(url)
        logger.info("Extracted %d features", len(feats))

        if len(feats) != len(expected):
            msg = f"Feature count mismatch: expected {len(expected)}, got {len(feats)}"
            logger.error(msg)
            return jsonify(error=msg), 400

        scaled = scaler.transform([feats])
        idx_phish = list(model.classes_).index(-1)
        prob = model.predict_proba(scaled)[0][idx_phish]
        threshold = 0.2
        result = "phishing" if prob > threshold else "legit"
        logger.info("Prob=%.4f, result=%s", prob, result)

        return jsonify(
            url=url,
            result=result,
            phishing_probability=round(prob,4),
            threshold=threshold
        )

    except Exception as e:
        logger.exception("Prediction error")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    # dev server; for production use gunicorn:
    app.run(host="0.0.0.0", port=5000, debug=False)
