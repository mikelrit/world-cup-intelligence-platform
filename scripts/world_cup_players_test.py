import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise ValueError("API_FOOTBALL_KEY not found.")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

OUTPUT_FOLDER = Path("api-tests/world-cup-results")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def save_file(filename, data):
    with open(
        OUTPUT_FOLDER / filename,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def test_players():
    url = f"{BASE_URL}/players"

    params = {
        "league": 1,
        "season": 2026,
        "page": 1
    }

    print("Testing World Cup players endpoint...")

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=60
    )

    print(f"HTTP Status: {response.status_code}")

    response.raise_for_status()

    data = response.json()

    print(f"Errors: {data.get('errors')}")
    print(f"Results: {data.get('results')}")
    print(f"Paging: {data.get('paging')}")

    save_file(
        "world_cup_players_test.json",
        data
    )

    print("Saved response.")


if __name__ == "__main__":
    test_players()