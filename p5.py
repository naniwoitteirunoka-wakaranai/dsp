import tkinter as tk
import random

root = tk.Tk()
root.title("Virus Simulation")
root.geometry("600x450")
root.configure(bg="#1e1e1e")

BG, FG, BTN = "#1e1e1e", "white", "#2563eb"

files = {f"File {i}.txt": "Safe" for i in range(1, 11)}
status = tk.StringVar(value="System Safe")

log = tk.Text(root, bg="#2b2b2b", fg="white", height=14)
log.pack(fill="both", padx=10, pady=10)

def update():
    log.delete("1.0", tk.END)
    for f, s in files.items():
        icon = "🟢" if s == "Safe" else "🔴" if s == "Infected" else "🟡"
        log.insert(tk.END, f"{icon} {f}  {s}\n")

def infect():
    random.choice(list(files.keys()))
    n = random.randint(2, 5)
    for f in random.sample(list(files.keys()), n):
        files[f] = "Infected"
    status.set("Virus Spread Simulation")
    update()

def scan():
    infected = [f for f, s in files.items() if s == "Infected"]
    if infected:
        for f in infected:
            files[f] = "Quarantined"
        status.set(f"Scan Complete  {len(infected)} Threats Quarantined")
    else:
        status.set("No Threats Found")
    update()

def clean():
    for f, s in files.items():
        if s == "Quarantined":
            files[f] = "Safe"
    status.set("System Clean")
    update()

tk.Label(root, text="Safe Educational Virus Simulation",
         bg=BG, fg=FG, font=("Arial", 13, "bold")).pack()

frame = tk.Frame(root, bg=BG)
frame.pack(pady=8)

buttons = [
    ("Spread Virus", infect),
    ("Scan System", scan),
    ("Clean System", clean)
]

for t, c in buttons:
    tk.Button(frame, text=t, command=c, bg=BTN, fg="white",
              width=16).pack(side="left", padx=5)

tk.Label(root, textvariable=status, bg=BG, fg="#00ff99",
         font=("Arial", 11, "bold")).pack(pady=10)

update()
root.mainloop()
