import pandas as pd
import re
import time
import numpy as np

# ---------- Sample Dataset ----------
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank"],
    "Age": [22, 24, 22, 23, 25, 24],
    "City": ["Bangalore", "Bangalore", "Bangalore",
             "Mysore", "Mysore", "Mysore"],
    "Email": ["alice@gmail.com", "bob@yahoo.com", "charlie@gmail.com",
              "david@gmail.com", "eva@yahoo.com", "frank@gmail.com"],
    "Phone": ["9876543210", "9123456789", "9988776655",
              "9876543211", "9123456790", "9988776666"],
    "Disease": ["Flu", "Diabetes", "Asthma",
                "Flu", "Diabetes", "Asthma"]
}

df = pd.DataFrame(data)

print("Original Data\n")
print(df)
time.sleep(1.5)

# ---------- PII Detection ----------
print("\nDetected PII\n")
for col in ["Name", "Email", "Phone"]:
    print(col)
time.sleep(1.5)

# ---------- Classification ----------
print("\nData Classification\n")
print("Data Type = Structured")
print("Data State = At Rest")
time.sleep(1.5)

# ---------- Basic Masking ----------
print("\nApplying PII Masking...\n")
time.sleep(1)

df["Name"] = "*****"
df["Email"] = df["Email"].apply(
    lambda x: re.sub(r"(^.).*(@.*)", r"\1****\2", x)
)
df["Phone"] = df["Phone"].str[:2] + "******" + df["Phone"].str[-2:]

print(df)
time.sleep(1.5)

# ---------- 1. k-Anonymity ----------
print("\nApplying k Anonymity...\n")
time.sleep(1)

df["Age"] = df["Age"].apply(lambda x: "20-25")

print("k Anonymity = Each generalized group contains multiple records")
print(df[["Age", "City"]])
time.sleep(1.5)

# ---------- 2. l-Diversity ----------
print("\nApplying l Diversity...\n")
time.sleep(1)

l_values = df.groupby(["Age", "City"])["Disease"].nunique()

print("Distinct sensitive values in each group")
print(l_values)

if all(l_values >= 3):
    print("l Diversity satisfied")
else:
    print("l Diversity not satisfied")

time.sleep(1.5)

# ---------- 3. t-Closeness ----------
print("\nApplying t Closeness...\n")
time.sleep(1)

overall = df["Disease"].value_counts(normalize=True)

for group, part in df.groupby(["Age", "City"]):
    group_dist = part["Disease"].value_counts(normalize=True)
    distance = sum(
        abs(overall.get(x, 0) - group_dist.get(x, 0))
        for x in overall.index
    ) / 2

    print(f"Group {group} Distance = {distance:.2f}")

print("t Closeness compares group distribution with overall distribution")
time.sleep(1.5)

# ---------- 4. Differential Privacy ----------
print("\nApplying Differential Privacy...\n")
time.sleep(1)

true_count = len(df)
epsilon = 1.0
noise = np.random.laplace(0, 1 / epsilon)
private_count = round(true_count + noise)

print("True Count ", true_count)
print("Privacy Epsilon ", epsilon)
print("Noisy Count ", private_count)

time.sleep(1.5)

# ---------- Final ----------
print("\nAnonymization Complete")
print(df)
