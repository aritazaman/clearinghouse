import json
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN is not set. Check your .env file.")

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}
# Load cases
with open("data/cases.json", "r") as f:
    cases = json.load(f)

# Find a case with a summary
for case in cases:
    if case.get("summary"):
        docs_url = case.get("case_documents_url")
        name = case.get("name")

        print(f"Case: {name}")
        print(f"URL: {docs_url}\n")

        response = requests.get(docs_url, headers=headers)

        print(f"Status: {response.status_code}")

        if response.ok:
            try:
                data = response.json()
                print(json.dumps(data, indent=2)[:3000])
            except requests.exceptions.JSONDecodeError:
                print("Invalid JSON response:")
                print(response.text[:1000])
        else:
            print("Request failed:")
            print(response.text[:1000])

        break
