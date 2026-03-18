import json
import requests
import os
import time
from dotenv import load_dotenv

# python3 -m venv .venv
# source .venv/bin/activate

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "User-Agent": "Chrome v22.2 Linux Ubuntu"
}

# Function to fetch all cases with pagination
def fetch_all_cases():
    all_cases = []
    url = "https://clearinghouse.net/api/v2p1/cases"
    retry_count = 0
    max_retries = 5
    
    while url and retry_count < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_cases.extend(data['results'])
            url = data.get('next')  # Next page URL
            retry_count = 0  # Reset on success
            print(f"Fetched {len(data['results'])} cases, total: {len(all_cases)}")
        elif response.status_code == 500:
            print(f"Server error 500, retrying... ({retry_count + 1}/{max_retries})")
            retry_count += 1
            time.sleep(5)  # Wait longer on error
        else:
            print(f"Error: {response.status_code}, stopping.")
            break
        time.sleep(1)  # Delay to avoid rate limit
    
    return all_cases

# Fetch all cases
cases = fetch_all_cases()
print(f"Total cases fetched: {len(cases)}")

# Try fetching documents list
doc_url = "https://clearinghouse.net/api/v2p1/documents"
response = requests.get(doc_url, headers=headers)
if response.status_code == 200:
    docs = response.json()
    print("Documents list:", json.dumps(docs, indent=2)[:1000])
else:
    print(f"Failed to fetch documents list: {response.status_code}")

# Save cases to file for training
with open("data/cases.json", "w") as f:
    json.dump(cases, f, indent=2)  

    