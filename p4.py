import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import hashlib, itertools, string, csv

root = tk.Tk()
root.title("Password Security")
root.geometry("650x520")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", troughcolor="#333", background="#00c853")

BG, FG, BTN = "#1e1e1e", "white", "#2563eb"

words = ["password","123456","admin","qwerty","letmein","welcome","abc123","dragon"]
status = tk.StringVar(value="Ready")
live = tk.StringVar()
target = tk.StringVar()

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def strength():
    p = target.get()
    score = sum([
        len(p) >= 8,
        any(i.isupper() for i in p),
        any(i.islower() for i in p),
        any(i.isdigit() for i in p),
        any(i in string.punctuation for i in p)
    ])
    msg = ["Weak","Weak","Medium","Medium","Strong","Strong"][score]
    status.set(f"Password Strength = {msg}")

def load_dict():
    global words
    f = filedialog.askopenfilename(filetypes=[("Text","*.txt")])
    if f:
        words = open(f, encoding="utf-8", errors="ignore").read().splitlines()
        status.set(f"Dictionary Loaded {len(words)} words")

def dictionary():
    h = target.get().strip()
    progress["value"] = 0
    for i, w in enumerate(words, 1):
        live.set(f"Trying {w}")
        progress["value"] = i / len(words) * 100
        root.update()
        if sha(w) == h or w == h:
            status.set(f"Password Found {w}")
            return
    status.set("Password Not Found")

def bruteforce():
    h = target.get().strip()
    chars = string.ascii_lowercase + string.digits
    total = sum(len(chars)**i for i in range(1,5))
    done = 0

    for l in range(1,5):
        for g in itertools.product(chars, repeat=l):
            p = "".join(g)
            done += 1
            live.set(f"Trying {p}")
            progress["value"] = done / total * 100
            root.update()
            if sha(p) == h or p == h:
                status.set(f"Password Found {p}")
                return
    status.set("Password Not Found")

def export(kind):
    p = filedialog.asksaveasfilename(defaultextension=f".{kind}")
    if not p:
        return
    if kind == "csv":
        with open(p, "w", newline="") as f:
            csv.writer(f).writerow(["Result", status.get()])
    else:
        open(p, "w").write(status.get())
    messagebox.showinfo("Done", "Report Saved")

# ---------- UI ----------
tk.Label(root, text="Password or SHA256 Hash", bg=BG, fg=FG,
         font=("Arial",12,"bold")).pack(pady=10)

tk.Entry(root, textvariable=target, width=55,
         bg="#333", fg="white", insertbackground="white").pack()

frame = tk.Frame(root, bg=BG)
frame.pack(pady=12)

buttons = [
    ("Check Strength", strength),
    ("Load Dictionary", load_dict),
    ("Dictionary Attack", dictionary),
    ("Brute Force", bruteforce),
    ("Export TXT", lambda: export("txt")),
    ("Export CSV", lambda: export("csv"))
]

for t, c in buttons:
    tk.Button(frame, text=t, command=c, bg=BTN, fg="white",
              width=18).pack(pady=4)

progress = ttk.Progressbar(root, length=560, mode="determinate")
progress.pack(pady=15)

tk.Label(root, textvariable=live, bg=BG, fg="#00ff99").pack()
tk.Label(root, textvariable=status, bg=BG, fg="cyan",
         font=("Arial",11,"bold")).pack(pady=15)

root.mainloop()
