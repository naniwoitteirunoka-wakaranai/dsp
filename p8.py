import tkinter as tk
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

root = tk.Tk()
root.title("Secure Messaging E2EE")
root.geometry("620x470")
root.configure(bg="#1e1e1e")

chat = tk.Text(root, bg="#2b2b2b", fg="white", height=18)
chat.pack(fill="both", padx=10, pady=10)

msg = tk.Entry(root, bg="#333", fg="white", insertbackground="white")
msg.pack(fill="x", padx=10, pady=5)

def server(cipher_text):
    chat.insert(tk.END, "Server Relay Encrypted Message\n")
    return cipher_text

def send():
    text = msg.get().strip()
    if not text:
        return

    encrypted = cipher.encrypt(text.encode())
    relay = server(encrypted)          # Server never decrypts
    decrypted = cipher.decrypt(relay).decode()

    chat.insert(tk.END, f"Alice  {text}\n")
    chat.insert(tk.END, f"Encrypted  {encrypted.decode()}\n")
    chat.insert(tk.END, f"Bob  {decrypted}\n")
    chat.insert(tk.END, "TLS Communication Simulated\n\n")

    msg.delete(0, tk.END)

tk.Label(root, text="End To End Encryption Messaging Demo",
         bg="#1e1e1e", fg="white",
         font=("Arial",12,"bold")).pack()

tk.Button(root, text="Send Message",
          command=send, bg="#2563eb", fg="white").pack(pady=8)

root.mainloop()
