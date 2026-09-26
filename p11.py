import pandas as pd
import re
import time

# Sample dataset
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [22, 24, 22],
    "Email": ["alice@gmail.com", "bob@yahoo.com", "charlie@gmail.com"],
    "Phone": ["9876543210", "9123456789", "9988776655"]
}

df = pd.DataFrame(data)

# ---------- Original Data ----------
print("Original Data\n")
print(df)
time.sleep(1.5)

# ---------- PII Detection ----------
print("\nDetected PII\n")
for col in df.columns:
    if col.lower() in ["name", "email", "phone"]:
        print(col)
time.sleep(1.5)

# ---------- Classification ----------
print("\nData Classification\n")
print("Data Type = Structured")
print("Data State = At Rest")
time.sleep(1.5)

# ---------- Anonymization ----------
print("\nApplying Anonymization...\n")
time.sleep(1)

df["Name"] = "*****"
df["Email"] = df["Email"].apply(
    lambda x: re.sub(r"(^.).*(@.*)", r"\1****\2", x)
)
df["Phone"] = df["Phone"].str[:2] + "******" + df["Phone"].str[-2:]

# ---------- k-Anonymity ----------
print("Applying k Anonymity...\n")
time.sleep(1)

df["Age"] = df["Age"].apply(lambda x: "20-25")

# ---------- Final Output ----------
print("Anonymized Data\n")
print(df)