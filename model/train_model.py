
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# ─── 1) Locate project root, data, and model dirs ─────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
data_dir    = os.path.join(project_root, "data")
model_dir   = os.path.join(project_root, "model")
os.makedirs(model_dir, exist_ok=True)

print(f"▶️ Loading data from: {data_dir}")
print(f"▶️ Saving model to : {model_dir}")

# ─── 2) Load the full-feature CSV ─────────────────────────────────────────────
csv_path = os.path.join(data_dir, "full_feature_dataset.csv")
df = pd.read_csv(csv_path)
print("🔍 Shape   :", df.shape)
print("🟢 Legit   :", (df["class"] == 1).sum())
print("🔴 Phish   :", (df["class"] == -1).sum())
print("❓ Missing :", df.isnull().any().any())

# ─── 3) Split into X / y ───────────────────────────────────────────────────────
X = df.drop(columns=["class"])
y = df["class"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ─── 4) Scale features ─────────────────────────────────────────────────────────
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ─── 5) Train Random Forest ───────────────────────────────────────────────────
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train_s, y_train)
print("✔️  Trained — Classes:", model.classes_)

# ─── 6) Evaluate ──────────────────────────────────────────────────────────────
y_pred = model.predict(X_test_s)
print("📊 Accuracy :", accuracy_score(y_test, y_pred))
print("📋 Report   :\n", classification_report(y_test, y_pred))

# ─── 7) Save model, scaler, and feature names ─────────────────────────────────
joblib.dump(model,  os.path.join(model_dir, "phishing_model.pkl"))
joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))

feat_file = os.path.join(model_dir, "feature_names.txt")
with open(feat_file, "w") as f:
    for col in X.columns:
        f.write(col + "\n")

print("✅ Model, scaler, and feature names written to:", model_dir)
