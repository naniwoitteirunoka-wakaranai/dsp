import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Vulnerability Analyzer")
root.geometry("650x450")
root.configure(bg="#1e1e1e")

BG, FG, BTN = "#1e1e1e", "white", "#2563eb"

patterns = {
    "Use of eval": "eval(",
    "Use of exec": "exec(",
    "SQL Injection Risk": "SELECT",
    "Hardcoded Password": "password",
    "OS Command Execution": "os.system",
    "Pickle Risk": "pickle.loads"
}

text = tk.Text(root, bg="#2b2b2b", fg="white")
text.pack(fill="both", expand=True, padx=10, pady=10)

def scan():
    file = filedialog.askopenfilename(
    filetypes=[
        ("Source Files", "*.py *.js *.java *.cpp *.c"),
        ("All Files", "*.*")
    ]
)
    if not file:
        return

    code = open(file, encoding="utf-8", errors="ignore").read()
    text.delete("1.0", tk.END)
    found = False

    for name, word in patterns.items():
        if word.lower() in code.lower():
            text.insert(tk.END, f"⚠ {name}\n")
            found = True

    if not found:
        text.insert(tk.END, "✅ No Common Vulnerabilities Found")

tk.Button(root, text="Select File and Scan",
          command=scan, bg=BTN, fg="white",
          width=22).pack(pady=8)

root.mainloop()
