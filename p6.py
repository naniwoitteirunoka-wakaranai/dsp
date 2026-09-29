import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Vulnerability Analyzer")
root.geometry("700x500")
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

text = tk.Text(
    root,
    bg="#2b2b2b",
    fg="white",
    insertbackground="white",
    font=("Consolas", 10)
)
text.pack(fill="both", expand=True, padx=10, pady=10)


def scan():
    file = filedialog.askopenfilename(
        filetypes=[
            ("Python", "*.py"),
            ("JavaScript", "*.js"),
            ("Java", "*.java"),
            ("C/C++", "*.c *.cpp"),
            ("All Files", "*.*")
        ]
    )

    if not file:
        return

    lines = open(
        file,
        encoding="utf-8",
        errors="ignore"
    ).readlines()

    text.delete("1.0", tk.END)

    text.insert(
        tk.END,
        "VULNERABILITY ANALYSIS REPORT\n"
        + "=" * 60
        + "\n\n"
    )

    found = False

    for no, line in enumerate(lines, 1):

        for name, word in patterns.items():

            if word.lower() in line.lower():

                text.insert(
                    tk.END,
                    f"Vulnerability  {name}\n"
                    f"Line Number    {no}\n"
                    f"Source Code    {line.strip()}\n"
                    + "-" * 60
                    + "\n"
                )

                found = True

    if not found:
        text.insert(
            tk.END,
            "No Common Vulnerabilities Found"
        )


title = tk.Label(
    root,
    text="Source Code Vulnerability Analyzer",
    bg=BG,
    fg=FG,
    font=("Arial", 15, "bold")
)
title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="Educational Demonstration using predefined vulnerability patterns",
    bg=BG,
    fg="#00ff99",
    font=("Arial", 10)
)
subtitle.pack()

tk.Button(
    root,
    text="Select File and Scan",
    command=scan,
    bg=BTN,
    fg="white",
    width=25
).pack(pady=10)

root.mainloop()
