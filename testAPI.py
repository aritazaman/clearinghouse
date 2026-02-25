import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# url = "https://clearinghouse.net/api/v2p1/test"
# response = requests.request("GET", url, headers=headers)
# print(response.text)

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "User-Agent": "Chrome v22.2 Linux Ubuntu"
}

url = "https://clearinghouse.net/api/v2p1/cases"
response = requests.get(url, headers=headers)

print("Status:", response.status_code)

data = response.json()
print(json.dumps(data, indent=2)[:2000])  

    