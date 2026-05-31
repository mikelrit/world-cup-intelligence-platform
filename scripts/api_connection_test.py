import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

url = "https://v3.football.api-sports.io/teams"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "id": 33
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)

data = response.json()

output_folder = Path("data/raw/teams")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "teams.json"

with open(output_file, "w") as file:
    json.dump(data, file, indent=4)

print("Saved to", output_file)