import os
import shutil
import joblib
import pandas as pd

from google.colab import drive, files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# 1. Google Drive
# =========================================================

drive.mount("/content/drive")

DRIVE_DIR = "/content/drive/MyDrive/PhishingDetection"

DATASET_PATH = os.path.join(
    DRIVE_DIR,
    "malicious_phish.csv"
)

MODEL_PATH = os.path.join(
    DRIVE_DIR,
    "phishing_tfidf_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    DRIVE_DIR,
    "phishing_tfidf_vectorizer.pkl"
)

os.makedirs(
    DRIVE_DIR,
    exist_ok=True
)


# =========================================================
# 2. Dataset
# =========================================================

if os.path.exists(DATASET_PATH):

    print("Dataset found in Google Drive")
    print("Using saved dataset")

else:

    print("Dataset not found in Google Drive")
    print("Please select the CSV file")

    uploaded = files.upload()

    uploaded_file = next(iter(uploaded))

    shutil.copy(
        uploaded_file,
        DATASET_PATH
    )

    print("Dataset saved to Google Drive")


# =========================================================
# 3. Load Dataset
# =========================================================

df = pd.read_csv(
    DATASET_PATH
)

print("\nOriginal Dataset")
print("Total URLs ", len(df))

print("\nCategories")
print(df["type"].value_counts())


# =========================================================
# 4. Keep Legitimate + Phishing
# =========================================================

df = df[
    df["type"].isin(
        ["benign", "phishing"]
    )
].copy()


# 0 = Legitimate
# 1 = Phishing

df["label"] = df["type"].map({
    "benign": 0,
    "phishing": 1
})

df["url"] = (
    df["url"]
    .fillna("")
    .astype(str)
    .str.strip()
)


print("\nPhishing Detection Dataset")
print("Total Records ", len(df))
print("Legitimate ", sum(df["label"] == 0))
print("Phishing ", sum(df["label"] == 1))


# =========================================================
# 5. Train / Test Split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    df["url"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)


# =========================================================
# 6. TF-IDF Feature Extraction
# =========================================================

print("\nCreating character-level TF-IDF features...")

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    min_df=2,
    max_features=200000,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(
    X_train
)

X_test_tfidf = vectorizer.transform(
    X_test
)

print(
    "Training Features ",
    X_train_tfidf.shape
)


# =========================================================
# 7. Train Logistic Regression
# =========================================================

print("\nTraining phishing detection model...")

model = LogisticRegression(
    max_iter=1000,
    C=2,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(
    X_train_tfidf,
    y_train
)


# =========================================================
# 8. Test Model
# =========================================================

predictions = model.predict(
    X_test_tfidf
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    "\nModel Accuracy ",
    round(
        accuracy * 100,
        2
    ),
    "%"
)

print("\nClassification Report")
print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Legitimate",
            "Phishing"
        ]
    )
)


# =========================================================
# 9. Save Model
# =========================================================

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    vectorizer,
    VECTORIZER_PATH
)

print("\nModel saved to Google Drive")
print(MODEL_PATH)

print("\nTF-IDF vectorizer saved to Google Drive")
print(VECTORIZER_PATH)


# =========================================================
# 10. Test New URL
# =========================================================

url = input(
    "\nEnter URL "
)

url_features = vectorizer.transform(
    [url]
)

result = model.predict(
    url_features
)[0]

probability = model.predict_proba(
    url_features
)[0]


# =========================================================
# 11. Display Prediction
# =========================================================

print("\nPrediction")

if result == 1:

    print(
        "Phishing Website"
    )

else:

    print(
        "Legitimate Website"
    )


print(
    "\nLegitimate Probability ",
    round(
        probability[0] * 100,
        2
    ),
    "%"
)

print(
    "Phishing Probability ",
    round(
        probability[1] * 100,
        2
    ),
    "%"
)
