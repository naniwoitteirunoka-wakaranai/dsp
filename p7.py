import os
import shutil
import joblib
import pandas as pd

from google.colab import drive, files
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# =========================================================
# 1. Mount Google Drive
# =========================================================

drive.mount("/content/drive")

DRIVE_DIR = "/content/drive/MyDrive/PhishingDetection"

DATASET_PATH = os.path.join(
    DRIVE_DIR,
    "malicious_phish.csv"
)

MODEL_PATH = os.path.join(
    DRIVE_DIR,
    "phishing_random_forest.pkl"
)

os.makedirs(DRIVE_DIR, exist_ok=True)


# =========================================================
# 2. Check Dataset
# =========================================================

if os.path.exists(DATASET_PATH):

    print("Dataset found in Google Drive")
    print("Using saved dataset")

else:

    print("Dataset not found in Google Drive")
    print("Please select the CSV you uploaded")

    uploaded = files.upload()

    uploaded_file = next(iter(uploaded))

    shutil.copy(
        uploaded_file,
        DATASET_PATH
    )

    print("Dataset saved to Google Drive")


# =========================================================
# 3. Check if Model Already Exists
# =========================================================

if os.path.exists(MODEL_PATH):

    print("\nSaved Random Forest model found")
    print("Loading model...")

    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully")


# =========================================================
# 4. Train Model if It Does Not Exist
# =========================================================

else:

    print("\nNo saved model found")
    print("Loading dataset...")

    df = pd.read_csv(DATASET_PATH)

    print("\nDataset Information")
    print("Total URLs ", len(df))
    print("\nCategories")
    print(df["type"].value_counts())


    # -----------------------------------------------------
    # Keep only legitimate and phishing URLs
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Extract URL Features
    # -----------------------------------------------------

    print("\nExtracting URL Features...")

    df["url_length"] = df["url"].apply(len)

    df["has_at"] = df["url"].apply(
        lambda x: int("@" in x)
    )

    df["has_https"] = df["url"].apply(
        lambda x: int(
            x.lower().startswith("https://")
        )
    )

    df["dot_count"] = df["url"].apply(
        lambda x: x.count(".")
    )

    df["slash_count"] = df["url"].apply(
        lambda x: x.count("/")
    )


    # -----------------------------------------------------
    # Select Features
    # -----------------------------------------------------

    feature_columns = [
        "url_length",
        "has_at",
        "has_https",
        "dot_count",
        "slash_count"
    ]

    X = df[feature_columns]
    y = df["label"]


    print("\nPhishing Detection Dataset")
    print("Total Records ", len(df))
    print("Legitimate ", sum(y == 0))
    print("Phishing ", sum(y == 1))


    # -----------------------------------------------------
    # Train / Test Split
    # -----------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


    # -----------------------------------------------------
    # Random Forest
    # -----------------------------------------------------

    print("\nTraining Random Forest...")

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )


    # -----------------------------------------------------
    # Accuracy
    # -----------------------------------------------------

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        "\nModel Accuracy ",
        round(accuracy * 100, 2),
        "%"
    )


    # -----------------------------------------------------
    # Save Model to Google Drive
    # -----------------------------------------------------

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("\nRandom Forest model saved to Google Drive")
    print(MODEL_PATH)


# =========================================================
# 5. Test a New URL
# =========================================================

url = input("\nEnter URL ")


features = pd.DataFrame([{

    "url_length": len(url),

    "has_at": int(
        "@" in url
    ),

    "has_https": int(
        url.lower().startswith("https://")
    ),

    "dot_count": url.count("."),

    "slash_count": url.count("/")

}])


# =========================================================
# 6. Predict
# =========================================================

result = model.predict(features)[0]


if result == 1:

    print("\nPrediction  Phishing Website")

else:

    print("\nPrediction  Legitimate Website")
