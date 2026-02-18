import json
import requests

API_TOKEN = ""  

# url = "https://clearinghouse.net/api/v2p1/test"

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "User-Agent": "Chrome v22.2 Linux Ubuntu"
}
# response = requests.request("GET", url, headers=headers)
# print(response.text)

url = "https://clearinghouse.net/api/v2p1/cases"
response = requests.get(url, headers=headers)

print("Status:", response.status_code)

data = response.json()
print(json.dumps(data, indent=2)[:2000])  

    