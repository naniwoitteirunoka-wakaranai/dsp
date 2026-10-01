import tkinter as tk
import socket
import ssl
import threading
import sys
import os
import datetime

from cryptography.fernet import Fernet
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


KEY_FILE = "secret.key"
PORT = 5000


# ---------------- E2EE KEY ----------------

if os.path.exists(KEY_FILE):
    KEY = open(KEY_FILE, "rb").read()
else:
    KEY = Fernet.generate_key()
    open(KEY_FILE, "wb").write(KEY)

cipher = Fernet(KEY)


# ---------------- TLS CERTIFICATE ----------------

if not os.path.exists("cert.pem"):

    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    name = x509.Name([
        x509.NameAttribute(
            NameOID.COMMON_NAME,
            "localhost"
        )
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(
            datetime.datetime.now(
                datetime.timezone.utc
            )
        )
        .not_valid_after(
            datetime.datetime.now(
                datetime.timezone.utc
            ) + datetime.timedelta(days=365)
        )
        .sign(
            private,
            hashes.SHA256()
        )
    )

    open("key.pem", "wb").write(
        private.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )
    )

    open("cert.pem", "wb").write(
        cert.public_bytes(
            serialization.Encoding.PEM
        )
    )


# ---------------- SERVER ----------------

def run_server():

    server = socket.socket()

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        ("0.0.0.0", PORT)
    )

    server.listen(2)

    ctx = ssl.SSLContext(
        ssl.PROTOCOL_TLS_SERVER
    )

    ctx.load_cert_chain(
        "cert.pem",
        "key.pem"
    )

    clients = []

    while len(clients) < 2:

        conn, _ = server.accept()

        conn = ctx.wrap_socket(
            conn,
            server_side=True
        )

        clients.append(conn)

    def relay(source, target):

        while True:

            try:

                data = source.recv(4096)

                if not data:
                    break

                # Relay encrypted data
                # Server never decrypts it
                target.sendall(data)

            except:
                break

    threading.Thread(
        target=relay,
        args=(clients[0], clients[1]),
        daemon=True
    ).start()

    threading.Thread(
        target=relay,
        args=(clients[1], clients[0]),
        daemon=True
    ).start()

    return clients[0]


# ---------------- GUI ----------------

root = tk.Tk()

root.title(
    "Secure E2EE Messaging"
)

root.geometry(
    "600x450"
)

root.minsize(
    500,
    350
)

root.configure(
    bg="#1e1e1e"
)


# Chat area expands
root.rowconfigure(
    0,
    weight=1
)

root.columnconfigure(
    0,
    weight=1
)


chat = tk.Text(
    root,
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"
)

chat.grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="nsew",
    padx=10,
    pady=10
)


# Message input

entry = tk.Entry(
    root,
    bg="#333",
    fg="white",
    insertbackground="white"
)

entry.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=(10, 5),
    pady=(0, 10)
)


root.columnconfigure(
    0,
    weight=1
)


# ---------------- CHAT FUNCTIONS ----------------

def show(message):

    root.after(
        0,
        lambda: chat.insert(
            tk.END,
            message + "\n"
        )
    )


def receive():

    while True:

        try:

            data = sock.recv(4096)

            if not data:
                break

            message = cipher.decrypt(
                data
            ).decode()

            show(
                "Peer  " + message
            )

        except:
            break


def send(event=None):

    text = entry.get().strip()

    if not text:
        return

    try:

        encrypted = cipher.encrypt(
            text.encode()
        )

        sock.sendall(
            encrypted
        )

        show(
            "You  " + text
        )

        entry.delete(
            0,
            tk.END
        )

    except:

        show(
            "Connection Error"
        )


entry.bind(
    "<Return>",
    send
)


# ---------------- CONNECTION ----------------

if len(sys.argv) < 2:

    print(
        "Use  python3 p8.py server"
    )

    print(
        "or    python3 p8.py client"
    )

    sys.exit()


if sys.argv[1] == "server":

    # Start relay server

    threading.Thread(
        target=run_server,
        daemon=True
    ).start()

    import time

    time.sleep(1)

    # Server process also becomes
    # the first chat client

    s = socket.socket()

    ctx = ssl.create_default_context()

    ctx.check_hostname = False

    ctx.verify_mode = ssl.CERT_NONE

    sock = ctx.wrap_socket(
        s,
        server_hostname="localhost"
    )

    sock.connect(
        ("127.0.0.1", PORT)
    )

else:

    s = socket.socket()

    ctx = ssl.create_default_context()

    ctx.check_hostname = False

    ctx.verify_mode = ssl.CERT_NONE

    sock = ctx.wrap_socket(
        s,
        server_hostname="localhost"
    )

    sock.connect(
        ("127.0.0.1", PORT)
    )


# ---------------- START CHAT ----------------

chat.insert(
    tk.END,
    "TLS Connected\n\n"
)


threading.Thread(
    target=receive,
    daemon=True
).start()


# Send button

tk.Button(
    root,
    text="Send",
    command=send,
    bg="#2563eb",
    fg="white",
    width=12
).grid(
    row=1,
    column=1,
    padx=(5, 10),
    pady=(0, 10)
)


root.mainloop()
