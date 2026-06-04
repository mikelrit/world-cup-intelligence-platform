import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

url = "https://v3.football.api-sports.io/standings"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "league": 39,
    "season": 2023
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)

data = response.json()

output_folder = Path("data/raw/fixtures")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "standings.json"

with open(output_file, "w") as file:
    json.dump(data, file, indent=4)

print("Saved to", output_file)