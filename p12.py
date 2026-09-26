import pandas as pd
import time

# ---------- GDPR vs DPDP ----------
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
}, index=["Region", "Individual Term", "Rights", "DPO"])

print("\nGDPR vs DPDP 2023 Comparison")
time.sleep(1)

while True:
    print("\nChoose an Option")
    print("1 View Comparison")
    print("2 Generate Incident Report")
    print("3 Exit")

    choice = input("\nEnter Choice ")

    if choice == "1":
        print("\nLoading Comparison...\n")
        time.sleep(1.5)
        print(df)

    elif choice == "2":
        print("\nGenerating Incident Report...\n")
        time.sleep(1.5)

        report = {
            "Incident ID": "INC001",
            "Date": "24 Sep 2026",
            "Type": "Data Breach",
            "Affected Data": "Name Email Phone",
            "Cause": "Unauthorized Access",
            "Action Taken": "Password Reset User Notified Access Blocked"
        }

        for k, v in report.items():
            print(f"{k} = {v}")
            time.sleep(0.8)

    elif choice == "3":
        break

    else:
        print("Invalid Choice")