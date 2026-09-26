import pandas as pd
import re

# Sample dataset
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [22, 24, 22],
    "Email": ["alice@gmail.com", "bob@yahoo.com", "charlie@gmail.com"],
    "Phone": ["9876543210", "9123456789", "9988776655"]
}

df = pd.DataFrame(data)

print("Original Data\n")
print(df)

# ---------- PII Detection ----------
print("\nDetected PII\n")

for col in df.columns:
    if col.lower() in ["name", "email", "phone"]:
        print(col)

# ---------- Classification ----------
print("\nData Type Structured")
print("Data State At Rest")

# ---------- Simple Anonymization ----------
df["Name"] = "*****"
df["Email"] = df["Email"].apply(lambda x: re.sub(r"(^.).*(@.*)", r"\1****\2", x))
df["Phone"] = df["Phone"].str[:2] + "******" + df["Phone"].str[-2:]

# ---------- k-Anonymity Style ----------
df["Age"] = df["Age"].apply(lambda x: "20-25")

print("\nAnonymized Data\n")
print(df)
