![logo](images/logo.png)



# Smart PhishBuster 

A real-time phishing detection system combining a browser extension and a Python machine learning backend. Detects phishing attempts by analyzing suspicious URLs, webpage content, and user behavior—using an ML model trained on thousands of real-world examples.

---

##  Features

- 30+ feature extraction from URLs, domain info, and page content
- Random Forest classifier (95% accuracy, balanced precision/recall)
- Flask API for fast /predict endpoint
- Chrome Extension for real-time site checks
- Whitelisting of trusted domains and popularity-based overrides
- Parallel, cached feature extraction for fast response times
- Full test suite and easy retraining pipeline

---

##  **Workflow Overview**

Workflow: ![workflow](images/workflow.png)
---

##   Screenshots


- Add your own screenshots here after uploading:

- Legitimate site verdict: ![Legit Verdict](images/legit.png)

- Phishing site warning: ![Phishing Verdict](images/phishing1.png)

- Phishing site warning: ![Phishing Verdict](images/phishing1.png)

- Feature extraction table/sample: ![Feature Extraction](./screenshot-features.png)

- Model training results: ![Results](./screenshot-results.png)

---

##  Installation

Clone the repo and set up a virtual environment:

```bash 
git clone <repo-url>
cd smart-phishbuster
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

##  Threshold Tuning
Model performance can be tuned by selecting a different decision threshold. Here are precision/recall values at various thresholds:
```bash
Threshold	Precision	Recall
0.00	    0.50	    1.00
0.01    	0.67     	1.00
0.02	    0.69    	0.99
0.04	    0.75	    0.99
0.07    	0.90	    0.98
0.11	    0.92    	0.98
0.14	    0.94    	0.98
0.32	    0.97    	0.97
0.68	    0.99    	0.94
0.87	    0.99    	0.93
0.90	    0.99    	0.89
0.93	    1.00    	0.86
0.98	    1.00    	0.81
1.00	    1.00    	0.76

Lower thresholds catch more phishing attempts (higher recall), while higher thresholds reduce false positives (higher precision). Choose based on your risk preference.
```

## 📈 Example Model Training Output
```
🔍 Shape   : (1992, 31)
🟢 Legit   : 995
🔴 Phish   : 997
❓ Missing : False
✔️  Trained — Classes: [-1  1]
📊 Accuracy : 0.9449
📋 Report   :
               precision    recall  f1-score   support

          -1       0.95      0.94      0.95       216
           1       0.94      0.95      0.94       183

    accuracy                           0.94       399

```

## 🏗️ Project Structure
```
Smart-Phish-Buster/
│
├── backend/
│   ├── app.py
│   ├── train.py
│   ├── generate_features.py
│   ├── threshold_tuning.py
│   ├── url_features.py
│   ├── model_loader.py
│   └── model/
│       ├── phishing_model.pkl
│       ├── scaler.pkl
│       └── feature_names.txt
│
├── data/
│   ├── PhiUSIIL_Phishing_URL_Dataset.csv
│   ├── full_feature_dataset.csv
│   └── balanced_dataset.csv
│
├── extension/
│   ├── manifest.json
│   ├── background.js
│   ├── popup.html
│   ├── popup.js
│   └── icon.png
│
├── tests/
│   ├── test_app.py
│   └── test_url_features.py
│
├── requirements.txt
├── README.md
```

## 📝 Limitations & Future Work
Most phishing URLs are dead (normal in research)

Occasional false positives on very long legit URLs (can be handled with more training data and whitelisting)

Can integrate real-time feeds (PhishTank/OpenPhish) for even fresher data

Deployment on cloud (Render/Heroku) and Chrome Web Store possible

---

## 🚦 Quickstart
Install requirements
```bash
python -m venv .venv
```
#
 Windows:
```
.venv\Scripts\activate
```
 macOS/Linux:
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```
Generate features, train the model

```bash
cd backend
python generate_features.py
python train.py
```
Run backend

```bash
python app.py
```
Load extension in Chrome

Go to chrome://extensions

Enable "Developer Mode"

Click "Load unpacked" and select the extension folder

Start testing live URLs!

---

## 📚 References
PhishTank

Kaggle Web Page Phishing Detection

scikit-learn docs

Flask

---

## 🪪 License
MIT License

----

## 💡 Questions or Issues?
Open an issue, or contact me at wheesk122@gmail.com

