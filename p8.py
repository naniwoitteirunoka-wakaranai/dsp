import tkinter as tk
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

root = tk.Tk()
root.title("Secure Chat E2EE")
root.geometry("600x450")
root.configure(bg="#1e1e1e")

chat = tk.Text(root, bg="#2b2b2b", fg="white", height=18)
chat.pack(fill="both", padx=10, pady=10)

msg = tk.Entry(root, bg="#333", fg="white", insertbackground="white")
msg.pack(fill="x", padx=10, pady=5)

def send():
    text = msg.get()
    if not text:
        return

    encrypted = cipher.encrypt(text.encode())      # Server receives this
    decrypted = cipher.decrypt(encrypted).decode() # Bob decrypts

    chat.insert(tk.END, f"You  {text}\n")
    chat.insert(tk.END, f"Encrypted  {encrypted.decode()}\n")
    chat.insert(tk.END, f"Bob  {decrypted}\n\n")
    msg.delete(0, tk.END)

tk.Button(root, text="Send Secure Message",
          command=send, bg="#2563eb", fg="white").pack(pady=8)

root.mainloop()
