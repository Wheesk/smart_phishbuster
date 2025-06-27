# Smart PhishBuster 🛡️

A real-time phishing detection system combining a browser extension and a Python machine learning backend. Detects phishing attempts by analyzing suspicious URLs, webpage content, and user behavior—using an ML model trained on thousands of real-world examples.

---

## 🚦 Features

- 30+ feature extraction from URLs, domain info, and page content
- Random Forest classifier (95% accuracy, balanced precision/recall)
- Flask API for fast /predict endpoint
- Chrome Extension for real-time site checks
- Whitelisting of trusted domains and popularity-based overrides
- Parallel, cached feature extraction for fast response times
- Full test suite and easy retraining pipeline

---

## 🗺️ **Workflow Overview**

```mermaid
flowchart LR
    A([Start]) --> B[User visits website]
    B --> C[Extension captures URL]
    C --> D[Send URL to backend API]
    D --> E{Is domain in whitelist?}
    E -- Yes --> F[Label as "legit" and show result]
    E -- No --> G[Extract URL + content features]
    G --> H[Run ML model (RandomForest)]
    H --> I{Phishing probability > threshold?}
    I -- Yes --> J[Label as "phishing"]
    I -- No --> K[Label as "legit"]
    J --> L[Display warning in extension]
    K --> F
    F --> M([End])
    L --> M




- ~2000 labeled URLs (1,000 phishing, 1,000 legit)
- Random Forest classifier, 95% accuracy on test set
- Real-world phishing detection with browser extension integration


## ⚡ Installation
Clone the repo and set up a virtual environment
```bash
git clone 
cd smart-phishbuster
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt


## 📈 Example Model Training Output
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


## 🏗️ Project Structure
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


##📝 Limitations & Future Work
Most phishing URLs are dead (normal in research)

Occasional false positives on very long legit URLs (can be handled with more training data and whitelisting)

Can integrate real-time feeds (PhishTank/OpenPhish) for even fresher data

Deployment on cloud (Render/Heroku) and Chrome Web Store possible

##📚 References
PhishTank

Kaggle Web Page Phishing Detection

scikit-learn docs

Flask

##🪪 License
MIT License

##🚦 Quickstart
Install requirements

Generate features, train the model

Run backend (python app.py)

Load extension in Chrome

Start testing live URLs!

##💡 Questions or Issues?
Open an issue, or contact me at [wheesk122@gmail.com]

