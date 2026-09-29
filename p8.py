import tkinter as tk
import socket, ssl, threading, sys, os, datetime
from cryptography.fernet import Fernet
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

KEY_FILE = "secret.key"

if os.path.exists(KEY_FILE):
    KEY = open(KEY_FILE, "rb").read()
else:
    KEY = Fernet.generate_key()
    open(KEY_FILE, "wb").write(KEY)

cipher = Fernet(KEY)

if not os.path.exists("cert.pem"):
    private = rsa.generate_private_key(65537, 2048)

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost")
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=365)
        )
        .sign(private, hashes.SHA256())
    )

    open("key.pem", "wb").write(
        private.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )
    )

    open("cert.pem", "wb").write(
        cert.public_bytes(serialization.Encoding.PEM)
    )

root = tk.Tk()
root.title("Secure E2EE Messaging")
root.geometry("600x450")
root.configure(bg="#1e1e1e")

chat = tk.Text(root, bg="#2b2b2b", fg="white")
chat.pack(fill="both", expand=True, padx=10, pady=10)

entry = tk.Entry(root, bg="#333", fg="white",
                 insertbackground="white")
entry.pack(fill="x", padx=10, pady=5)

def receive():
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            chat.insert(
                tk.END,
                "Peer  " + cipher.decrypt(data).decode() + "\n"
            )
        except:
            break

def send():
    text = entry.get().strip()
    if text:
        sock.sendall(cipher.encrypt(text.encode()))
        chat.insert(tk.END, "You  " + text + "\n")
        entry.delete(0, tk.END)

if sys.argv[1] == "server":
    s = socket.socket()
    s.bind(("0.0.0.0", 5000))
    s.listen(1)

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("cert.pem", "key.pem")

    conn, _ = s.accept()
    sock = ctx.wrap_socket(conn, server_side=True)

else:
    s = socket.socket()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    sock = ctx.wrap_socket(s, server_hostname="localhost")
    sock.connect(("127.0.0.1", 5000))

chat.insert(tk.END, "TLS Connected\n\n")

threading.Thread(
    target=receive,
    daemon=True
).start()

tk.Button(
    root, text="Send", command=send,
    bg="#2563eb", fg="white", width=12
).pack(pady=8)

root.mainloop()
