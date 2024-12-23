import requests
import json
import os

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    api_key = "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" # Hardcode it here if not set in env vars

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

url = "https://api.groq.com/openai/v1/chat/completions"

payload = {
    "model": "llama3-8b-8192", 
    "messages": [
        {"role": "user", "content": "Hello, how can I assist with sales?"}
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(payload))


if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)


