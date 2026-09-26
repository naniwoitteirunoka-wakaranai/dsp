from flask import Flask, request
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)
SECRET = "ai_lab"

# ---------- RSA Digital Signature ----------
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

message = b"Secure Banking Transaction"

signature = private_key.sign(
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

try:
    public_key.verify(
        signature, message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("Digital Signature Verified")
except:
    print("Signature Verification Failed")

# ---------- JWT Authentication ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "student" and data["password"] == "1234":
        return {"token": jwt.encode({"user": "student"}, SECRET, algorithm="HS256")}
    return {"message": "Login Failed"}, 401

@app.route("/secure")
def secure():
    try:
        token = request.headers["Authorization"]
        user = jwt.decode(token, SECRET, algorithms=["HS256"])
        return {"message": f"Welcome {user['user']}"}
    except:
        return {"message": "Unauthorized"}, 401

app.run(debug=True)
