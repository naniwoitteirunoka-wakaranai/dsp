# Simple Password Strength Checker
password = input("Enter password ")
if len(password) >= 8:
print("Password length is good")
else:
print("Weak password, Use at least 8 characters")
# Introduction to TryHackMe:Basic User Authentication Simulation
username = input("Enter username ")
password = input("Enter password ")
if username == "cat" and password == "meow1234":
print("Login Successful")
else:
print("Invalid Username or Password")
# Find Local IP Address
import socket
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("Hostname ", hostname)
print("Local IP Address ", ip_address)
# Simple Caesar Cipher
text = input("Enter message ")
shift = 3
encrypted = ""
for char in text:
encrypted += chr(ord(char) + shift)
print("Encrypted Message ", encrypted)
# Hex Encoding and Decoding
text = "Hello"
encoded = text.encode().hex()
print("Encoded ", encoded)
decoded = bytes.fromhex(encoded).decode()
print("Decoded ", decoded)
