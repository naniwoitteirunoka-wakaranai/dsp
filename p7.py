import os, shutil, joblib, numpy as np, pandas as pd
from google.colab import drive, files
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer, MaxAbsScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. Google Drive
drive.mount("/content/drive")
DRIVE_DIR = "/content/drive/MyDrive/PhishingDetection"
DATASET_PATH = os.path.join(DRIVE_DIR, "malicious_phish.csv")
MODEL_PATH = os.path.join(DRIVE_DIR, "phishing_model.pkl")
os.makedirs(DRIVE_DIR, exist_ok=True)

# 2. Dataset
if os.path.exists(DATASET_PATH):
    print("Dataset found in Google Drive")
else:
    print("Dataset not found. Please select the CSV file")
    uploaded = files.upload()
    shutil.copy(next(iter(uploaded)), DATASET_PATH)
    print("Dataset saved to Google Drive")

# 3. Load + clean (0 = legit, 1 = phishing)
clean = lambda s: (s.fillna("").astype(str).str.strip().str.lower()
                   .str.replace(r"^https?://", "", regex=True)
                   .str.replace(r"^www\.", "", regex=True))

df = pd.read_csv(DATASET_PATH)
df = df[df["type"].isin(["benign", "phishing"])].copy()
df["label"] = df["type"].map({"benign": 0, "phishing": 1})
df["url"] = clean(df["url"])
print(df["label"].value_counts())

# 4. Split
X_train, X_test, y_train, y_test = train_test_split(
    df["url"], df["label"], test_size=0.2, random_state=42, stratify=df["label"])

# 5. Handcrafted features (length, @, dots, hyphens, digits, IP, ...)
def feats(urls):
    s = pd.Series(list(urls))
    return np.c_[
        s.str.len(), s.str.count("@"), s.str.count(r"\."), s.str.count("-"),
        s.str.count(r"\d"), s.str.count("/"), s.str.count(r"\?"), s.str.count("="),
        s.str.contains(r"^\d+\.\d+\.\d+\.\d+"),
    ].astype(float)

# 6. Model: char n-gram TF-IDF + handcrafted features -> Logistic Regression
model = Pipeline([
    ("features", FeatureUnion([
        ("ngrams", TfidfVectorizer(analyzer="char", ngram_range=(3, 5),
                                   min_df=2, max_features=300000, sublinear_tf=True)),
        ("hand", Pipeline([("f", FunctionTransformer(feats)), ("s", MaxAbsScaler())])),
    ])),
    ("clf", LogisticRegression(C=10, max_iter=1000, class_weight="balanced")),
])

print("\nTraining...")
model.fit(X_train, y_train)

# 7. Evaluate
print(classification_report(y_test, model.predict(X_test),
                            target_names=["Legitimate", "Phishing"]))

# 8. Save
joblib.dump(model, MODEL_PATH)
print("Model saved:", MODEL_PATH)

# 9. Test new URL
TRUSTED = {"google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
           "microsoft.com", "apple.com", "github.com", "linkedin.com", "twitter.com"}

url = clean(pd.Series([input("\nEnter URL ")]))[0]
host = url.split("/")[0].split(":")[0]

if host in TRUSTED:
    print("\nPrediction: Legitimate Website (trusted domain)")
else:
    p = model.predict_proba([url])[0]
    print("\nPrediction:", "Phishing Website" if p[1] > 0.5 else "Legitimate Website")
    print(f"Legitimate: {p[0]*100:.2f}%  |  Phishing: {p[1]*100:.2f}%")
