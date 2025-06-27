import joblib
import os

def load_model_and_scaler():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR = os.path.join(BASE_DIR, 'model')

    try:
        model = joblib.load(os.path.join(MODEL_DIR, 'phishing_model.pkl'))
        scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    except Exception as e:
        raise FileNotFoundError(f"❌ Model or scaler file missing: {e}")

    return model, scaler

def load_feature_names():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, 'model', 'feature_names.txt')
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return [line.strip() for line in f.readlines()]
