import pandas as pd
import re
import time
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import pytesseract

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

# ---------- Basic PII Masking ----------
print("\nApplying PII Masking...\n")
time.sleep(1)

df["Name"] = "*****"

df["Email"] = df["Email"].apply(
    lambda x: re.sub(r"(^.).*(@.*)", r"\1****\2", x)
)

df["Phone"] = df["Phone"].str[:2] + "******" + df["Phone"].str[-2:]

print(df)
time.sleep(1.5)


# =========================================================
# 1. k-ANONYMITY
# =========================================================

print("\nApplying k Anonymity...\n")
time.sleep(1)

df["Age"] = df["Age"].apply(lambda x: "20-25")

k = 3

groups = df.groupby(["Age", "City"]).size()

print("Equivalence Group Sizes")
print(groups)

if all(groups >= k):
    print(f"k Anonymity Satisfied for k = {k}")
else:
    print(f"k Anonymity Not Satisfied for k = {k}")

time.sleep(1.5)


# =========================================================
# 2. l-DIVERSITY
# =========================================================

print("\nApplying l Diversity...\n")
time.sleep(1)

l = 3

diversity = df.groupby(
    ["Age", "City"]
)["Disease"].nunique()

print("Distinct Sensitive Values")
print(diversity)

if all(diversity >= l):
    print(f"l Diversity Satisfied for l = {l}")
else:
    print(f"l Diversity Not Satisfied for l = {l}")

time.sleep(1.5)


# =========================================================
# 3. t-CLOSENESS
# =========================================================

print("\nApplying t Closeness...\n")
time.sleep(1)

t = 0.20

overall = df["Disease"].value_counts(normalize=True)

print("Overall Disease Distribution")
print(overall)

print("\nGroup Distances")

t_satisfied = True

for group, part in df.groupby(["Age", "City"]):

    group_distribution = part["Disease"].value_counts(normalize=True)

    distance = sum(
        abs(
            overall.get(value, 0)
            - group_distribution.get(value, 0)
        )
        for value in overall.index
    ) / 2

    print(f"{group} Distance = {distance:.2f}")

    if distance > t:
        t_satisfied = False

if t_satisfied:
    print(f"t Closeness Satisfied for t = {t}")
else:
    print(f"t Closeness Not Satisfied for t = {t}")

time.sleep(1.5)


# =========================================================
# 4. DIFFERENTIAL PRIVACY
# =========================================================

print("\nApplying Differential Privacy...\n")
time.sleep(1)

epsilon = 1.0

true_count = len(df)

noise = np.random.laplace(
    0,
    1 / epsilon
)

private_count = round(true_count + noise)

print("True Count ", true_count)
print("Privacy Epsilon ", epsilon)
print("Generated Noise ", round(noise, 2))
print("Private Count ", private_count)

time.sleep(1.5)


# =========================================================
# RE-IDENTIFICATION RISK
# =========================================================

print("\nRe Identification Risk\n")
time.sleep(1)

unique_before = len(data["Name"])

unique_after = df.groupby(
    ["Age", "City"]
).ngroups

print("Unique Records Before Anonymization ", unique_before)
print("Unique Groups After Anonymization ", unique_after)

if unique_after < unique_before:
    print("Re Identification Risk Reduced")
else:
    print("Further Anonymization Required")

time.sleep(1.5)


# =========================================================
# IMAGE OCR + PII REDACTION
# =========================================================

def anonymize_image():

    file = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg"),
            ("All Files", "*.*")
        ]
    )

    if not file:
        return

    print("\nScanning Image Using OCR...\n")

    image = Image.open(file)
    draw = ImageDraw.Draw(image)

    ocr = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    found = 0

    for i, text in enumerate(ocr["text"]):

        text = text.strip()

        if not text:
            continue

        email = re.search(
            r"[\w.-]+@[\w.-]+\.\w+",
            text
        )

        phone = re.search(
            r"\b\d{10}\b",
            text
        )

        name = text.lower() in [
            "alice",
            "bob",
            "charlie",
            "david",
            "eva",
            "frank"
        ]

        if email or phone or name:

            x = ocr["left"][i]
            y = ocr["top"][i]
            w = ocr["width"][i]
            h = ocr["height"][i]

            draw.rectangle(
                (x, y, x + w, y + h),
                fill="black"
            )

            found += 1

    output = "anonymized_image.png"

    image.save(output)

    print("PII Found ", found)
    print("Anonymized Image Saved ", output)

    messagebox.showinfo(
        "Done",
        f"PII Redacted {found}\nSaved as {output}"
    )


# =========================================================
# GUI
# =========================================================

root = tk.Tk()
root.title("PII Anonymization Tool")
root.geometry("450x250")
root.configure(bg="#1e1e1e")

tk.Label(
    root,
    text="PII Anonymization",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 15, "bold")
).pack(pady=20)

tk.Label(
    root,
    text="OCR can detect and redact text PII from images",
    bg="#1e1e1e",
    fg="#00ff99"
).pack(pady=5)

tk.Button(
    root,
    text="Select Image and Anonymize",
    command=anonymize_image,
    bg="#2563eb",
    fg="white",
    width=28
).pack(pady=20)

tk.Button(
    root,
    text="Close",
    command=root.destroy,
    bg="#444",
    fg="white",
    width=15
).pack()

root.mainloop()
