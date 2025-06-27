# threshold_tuning.py

import joblib
import pandas as pd
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt

# ─── 1) Load data, scaler, and model ───────────────────────────────────────────
df     = pd.read_csv("data/full_feature_dataset.csv")
model  = joblib.load("model/phishing_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# features / labels
X = df.drop(columns=["class"])
y = (df["class"] == -1).astype(int)     # here: phishing=1, legit=0

# scale
X_s = scaler.transform(X)

# ─── 2) Compute probabilities for the “phishing” class ─────────────────────────
phish_idx = list(model.classes_).index(-1)
probs     = model.predict_proba(X_s)[:, phish_idx]

# ─── 3) ROC Curve ──────────────────────────────────────────────────────────────
fpr, tpr, roc_thresh = roc_curve(y, probs)
roc_auc              = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0,1],[0,1], "--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()

# ─── 4) Precision–Recall Curve ─────────────────────────────────────────────────
precision, recall, pr_thresh = precision_recall_curve(y, probs)
pr_auc                     = auc(recall, precision)

plt.figure()
plt.plot(recall, precision, label=f"PR AUC = {pr_auc:.2f}")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curve")
plt.legend()
plt.show()

# ─── 5) Print a few candidate thresholds ────────────────────────────────────────
print("\nSample thresholds and metrics:")
for p, r, t in zip(precision[::10], recall[::10], pr_thresh[::10]):
    print(f" thresh={t:.2f}  → precision={p:.2f}, recall={r:.2f}")
