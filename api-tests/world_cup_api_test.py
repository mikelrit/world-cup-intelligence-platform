import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise ValueError("API_FOOTBALL_KEY was not found in the .env file.")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

LEAGUE_ID = 1
SEASON = 2026

OUTPUT_FOLDER = Path("api-tests/world-cup-results")


def request_endpoint(endpoint: str, params: dict) -> dict:
    """Request one API-Football endpoint and validate its response."""

    url = f"{BASE_URL}/{endpoint}"

    print(f"\nTesting /{endpoint}")
    print(f"Parameters: {params}")

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30
    )

    print(f"HTTP status: {response.status_code}")

    response.raise_for_status()

    data = response.json()

    api_errors = data.get("errors", {})

    if api_errors:
        print(f"API errors: {api_errors}")
    else:
        print("API errors: none")

    print(f"Results returned: {data.get('results', 0)}")
    print(f"Paging: {data.get('paging', {})}")

    return data


def save_response(filename: str, data: dict) -> None:
    """Save a test response for manual inspection."""

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_FOLDER / filename

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved test response to {output_file}")


def main() -> None:
    teams_data = request_endpoint(
        endpoint="teams",
        params={
            "league": LEAGUE_ID,
            "season": SEASON
        }
    )

    save_response(
        "world_cup_teams_test.json",
        teams_data
    )

    fixtures_data = request_endpoint(
        endpoint="fixtures",
        params={
            "league": LEAGUE_ID,
            "season": SEASON
        }
    )

    save_response(
        "world_cup_fixtures_test.json",
        fixtures_data
    )

    standings_data = request_endpoint(
        endpoint="standings",
        params={
            "league": LEAGUE_ID,
            "season": SEASON
        }
    )

    save_response(
        "world_cup_standings_test.json",
        standings_data
    )

    print("\nWorld Cup API test complete.")
    print("Inspect the files inside api-tests/world-cup-results/.")


if __name__ == "__main__":
    main()