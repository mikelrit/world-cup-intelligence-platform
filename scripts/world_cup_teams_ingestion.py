import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise ValueError(
        "API_FOOTBALL_KEY was not found. Check your .env file."
    )

BASE_URL = "https://v3.football.api-sports.io"
ENDPOINT = "/teams"

LEAGUE_ID = 1
SEASON = 2026

HEADERS = {
    "x-apisports-key": API_KEY
}

PARAMS = {
    "league": LEAGUE_ID,
    "season": SEASON
}

OUTPUT_FOLDER = Path("data/raw/world_cup/teams")
OUTPUT_FILE = OUTPUT_FOLDER / "world_cup_teams_raw.json"


def fetch_world_cup_teams() -> dict:
    """Retrieve all 2026 World Cup teams from API-Football."""

    url = f"{BASE_URL}{ENDPOINT}"

    print("Requesting 2026 World Cup teams...")

    response = requests.get(
        url,
        headers=HEADERS,
        params=PARAMS,
        timeout=30
    )

    print(f"HTTP status: {response.status_code}")

    response.raise_for_status()

    data = response.json()

    api_errors = data.get("errors", {})

    if api_errors:
        raise RuntimeError(f"API returned errors: {api_errors}")

    teams = data.get("response", [])

    if not teams:
        raise RuntimeError(
            "The API returned zero World Cup teams."
        )

    print(f"Teams received: {len(teams)}")

    return data


def save_raw_data(data: dict) -> None:
    """Save the untouched API response to the Raw layer."""

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Saved raw teams data to: {OUTPUT_FILE}")


def main() -> None:
    data = fetch_world_cup_teams()
    save_raw_data(data)

    print("World Cup teams ingestion completed successfully.")


if __name__ == "__main__":
    main()