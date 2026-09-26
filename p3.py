import hashlib, threading, time
from cryptography.fernet import Fernet

# ---------- Confidentiality ----------
msg = "Top Secret: AI is amazing!"
key = Fernet.generate_key()
cipher = Fernet(key)
enc = cipher.encrypt(msg.encode())

print("\n--- Confidentiality ---")
print("Original ", msg)
print("Encrypted ", enc)
print("Decrypted ", cipher.decrypt(enc).decode())

# ---------- Integrity ----------
print("\n--- Integrity ---")
h1 = hashlib.sha256(msg.encode()).hexdigest()
h2 = hashlib.sha256("Top Secret: AI hacked!".encode()).hexdigest()

print("Original Hash ", h1)
print("Tampered Hash ", h2)
print("Integrity OK" if h1 == h2 else "Integrity Breach!")

# ---------- Availability ----------
print("\n--- Availability ---")

def server():
    while True:
        print("Server Running...")
        time.sleep(1)

threading.Thread(target=server, daemon=True).start()

time.sleep(3)
print("Simulating DDoS Attack...")
time.sleep(2)
print("Server Busy...")
time.sleep(2)
print("Server Restored!")

time.sleep(3)
