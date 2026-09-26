import pandas as pd

# ---------- GDPR vs DPDP 2023 ----------
df = pd.DataFrame({
    "GDPR": [
        "European Union",
        "Data Subject",
        "Right to Access Delete Correct",
        "DPO Required"
    ],
    "DPDP 2023": [
        "India",
        "Data Principal",
        "Right to Access Correct Erase",
        "DPO for Significant Data Fiduciary"
    ]
}, index=[
    "Region",
    "Individual Term",
    "Rights",
    "DPO"
])

print("\nGDPR vs DPDP 2023\n")
print(df)

# ---------- Mock Incident Report ----------
print("\nMock Incident Report\n")

report = {
    "Incident ID": "INC001",
    "Date": "24 Sep 2026",
    "Type": "Data Breach",
    "Affected Data": "Name Email Phone",
    "Cause": "Unauthorized Access",
    "Action Taken": "Password Reset User Notified Access Blocked"
}

for k, v in report.items():
    print(f"{k}  {v}")
