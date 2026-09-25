# Check System Information
import platform
print("Operating System ", platform.system())
print("Version ", platform.version())
print("Machine ", platform.machine())

# Network Traffic Analysis Using Wireshark
import requests
website = "https://example.com"
response = requests.get(website)
print("Status Code:", response.status_code)

# Simple Input Validation
username = input("Enter username ")
if username.isalnum():
   print("Valid Input")
else:
   print("Invalid Input, Special characters detected")
# Simple SQL Injection Keyword Detection
user_input = input("Enter username ")
keywords = ["SELECT", "DROP", "DELETE", "--"]
for word in keywords:
if word.lower() in user_input.lower():
   print("Possible malicious input detected")
   break
else:
   print("Input appears normal")
