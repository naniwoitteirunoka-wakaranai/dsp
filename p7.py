import os
import shutil
import joblib
import pandas as pd
import ipaddress

from urllib.parse import urlparse
from google.colab import drive, files
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


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
    "phishing_random_forest.pkl"
)

os.makedirs(DRIVE_DIR, exist_ok=True)


# =========================================================
# 2. Model Version
# =========================================================

MODEL_VERSION = 2


# =========================================================
# 3. Check Dataset
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
# 4. URL Feature Extraction
# =========================================================

def extract_features(url):

    url = str(url).strip()

    hostname = ""
    path = ""

    try:

        if not url.startswith(
            ("http://", "https://")
        ):
            url = "http://" + url

        parsed = urlparse(url)

        try:
            hostname = parsed.hostname or ""
        except ValueError:
            hostname = ""

        path = parsed.path or ""

    except ValueError:

        # Handles malformed URLs
        pass


    # -----------------------------------------------------
    # Check for IP address
    # -----------------------------------------------------

    try:

        ipaddress.ip_address(hostname)
        has_ip = 1

    except (ValueError, TypeError):

        has_ip = 0


    # -----------------------------------------------------
    # Suspicious words
    # -----------------------------------------------------

    suspicious_words = [
        "login",
        "verify",
        "verification",
        "secure",
        "account",
        "update",
        "confirm",
        "bank",
        "signin",
        "password",
        "credential",
        "wallet",
        "payment"
    ]

    suspicious_count = sum(
        word in url.lower()
        for word in suspicious_words
    )


    # -----------------------------------------------------
    # Return features
    # -----------------------------------------------------

    return {

        "url_length": len(url),

        "hostname_length": len(hostname),

        "path_length": len(path),

        "dot_count": url.count("."),

        "hyphen_count": url.count("-"),

        "digit_count": sum(
            c.isdigit()
            for c in url
        ),

        "at_count": url.count("@"),

        "question_count": url.count("?"),

        "equal_count": url.count("="),

        "slash_count": url.count("/"),

        "has_https": int(
            url.lower().startswith("https://")
        ),

        "has_ip": has_ip,

        "subdomain_count": max(
            0,
            len(hostname.split(".")) - 2
        ),

        "suspicious_words": suspicious_count
    }


# =========================================================
# 5. Load Saved Model
# =========================================================

model = None

if os.path.exists(MODEL_PATH):

    print("\nSaved Random Forest model found")

    saved = joblib.load(
        MODEL_PATH
    )

    if (
        isinstance(saved, dict)
        and saved.get("version") == MODEL_VERSION
    ):

        model = saved["model"]

        print("Model version is current")
        print("Loading saved model...")
        print("Model loaded successfully")

    else:

        print("Old model detected")
        print("Retraining with improved features...")


# =========================================================
# 6. Train Model
# =========================================================

if model is None:

    print("\nLoading dataset...")

    df = pd.read_csv(
        DATASET_PATH
    )


    print("\nDataset Information")

    print(
        "Total URLs ",
        len(df)
    )

    print("\nCategories")

    print(
        df["type"].value_counts()
    )


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
    # Extract Features
    # -----------------------------------------------------

    print("\nExtracting URL features...")

    feature_data = df["url"].apply(
        extract_features
    )

    X = pd.DataFrame(
        feature_data.tolist()
    )

    y = df["label"]


    print("\nPhishing Detection Dataset")

    print(
        "Total Records ",
        len(df)
    )

    print(
        "Legitimate ",
        sum(y == 0)
    )

    print(
        "Phishing ",
        sum(y == 1)
    )


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

        n_estimators=150,

        max_depth=15,

        random_state=42,

        n_jobs=-1,

        class_weight="balanced"

    )


    model.fit(

        X_train,

        y_train

    )


    # -----------------------------------------------------
    # Accuracy
    # -----------------------------------------------------

    predictions = model.predict(
        X_test
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


    # -----------------------------------------------------
    # Save Model
    # -----------------------------------------------------

    saved_model = {

        "version": MODEL_VERSION,

        "features": list(
            X.columns
        ),

        "model": model

    }


    joblib.dump(

        saved_model,

        MODEL_PATH

    )


    print(
        "\nNew Random Forest model saved"
    )

    print(
        MODEL_PATH
    )


# =========================================================
# 7. Enter URL
# =========================================================

url = input(
    "\nEnter URL "
)


# =========================================================
# 8. Extract Features
# =========================================================

features = pd.DataFrame([

    extract_features(url)

])


# =========================================================
# 9. Prediction
# =========================================================

result = model.predict(

    features

)[0]


probability = model.predict_proba(

    features

)[0]


legitimate_probability = (
    probability[0] * 100
)

phishing_probability = (
    probability[1] * 100
)


# =========================================================
# 10. Display Result
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
        legitimate_probability,
        2
    ),
    "%"
)


print(

    "Phishing Probability ",

    round(
        phishing_probability,
        2
    ),
    "%"
)
