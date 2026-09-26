import hashlib, base64

# ---------- Hash Functions ----------
text = input("Enter Text ")

print("\nMD5 Hash")
print(hashlib.md5(text.encode()).hexdigest())

print("\nSHA256 Hash")
print(hashlib.sha256(text.encode()).hexdigest())

# ---------- Simple Obfuscation ----------
code = 'print("Hello from Hidden Function")'

encoded = base64.b64encode(code.encode()).decode()
print("\nObfuscated Code")
print(encoded)

print("\nExecuting Hidden Code")
exec(base64.b64decode(encoded).decode())
