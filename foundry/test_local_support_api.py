import requests

payload = {
    "question": "How do I log in?",
    "top": 3,
}

response = requests.post("http://127.0.0.1:8000/ask", json=payload, timeout=15)
response.raise_for_status()

data = response.json()

print("Local support API worked.")
print("Answer:", data["response"]["answer"])
print("Next steps:", data["response"]["next_steps"])
print("Confidence:", data["response"]["confidence"])