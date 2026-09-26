from flask import Flask, request
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)
SECRET = "AI73"

private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public = private.public_key()

message = b"E Commerce Transaction"

signature = private.sign(
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

try:
    public.verify(
        signature, message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("Digital Signature Verified")
except:
    print("Verification Failed")

@app.route("/login", methods=["POST"])
def login():
    d = request.json
    if d["username"] == "student" and d["password"] == "1234":
        token = jwt.encode({"user": "student"}, SECRET, algorithm="HS256")
        return {"token": token}
    return {"message": "Login Failed"}, 401

@app.route("/secure")
def secure():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user = jwt.decode(token, SECRET, algorithms=["HS256"])
        return {"message": f"Access Granted {user['user']}"}
    except:
        return {"message": "Unauthorized"}, 401

app.run(debug=True)
