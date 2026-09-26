import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Sample dataset
data = {
    "length": [12, 45, 18, 60, 22, 75],
    "has_at": [0, 1, 0, 1, 0, 1],
    "https": [1, 0, 1, 0, 1, 0],
    "label": [0, 1, 0, 1, 0, 1]   # 0 Legit, 1 Phishing
}

df = pd.DataFrame(data)

X = df[["length", "has_at", "https"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# User Input
url = input("Enter URL ")

features = [[
    len(url),
    int("@" in url),
    int(url.startswith("https"))
]]

result = model.predict(features)[0]

print("\nPrediction", "Phishing Website" if result else "Legitimate Website")
print("Accuracy", round(model.score(X_test, y_test) * 100, 2), "%")
