import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise ValueError(
        "API_FOOTBALL_KEY was not found. Check your .env file."
    )

BASE_URL = "https://v3.football.api-sports.io"
ENDPOINT = "/fixtures"

LEAGUE_ID = 1
SEASON = 2026

HEADERS = {
    "x-apisports-key": API_KEY
}

PARAMS = {
    "league": LEAGUE_ID,
    "season": SEASON
}

OUTPUT_FOLDER = Path(
    "data/raw/world_cup/fixtures"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_fixtures_raw.json"
)


def fetch_world_cup_fixtures() -> dict[str, Any]:
    """Retrieve all 2026 FIFA World Cup fixtures."""

    url = f"{BASE_URL}{ENDPOINT}"

    print("Requesting 2026 World Cup fixtures...")

    response = requests.get(
        url,
        headers=HEADERS,
        params=PARAMS,
        timeout=60
    )

    print(f"HTTP status: {response.status_code}")

    response.raise_for_status()

    data = response.json()

    api_errors = data.get("errors", {})

    if api_errors:
        raise RuntimeError(
            f"API returned errors: {api_errors}"
        )

    fixtures = data.get("response", [])

    if not fixtures:
        raise RuntimeError(
            "The API returned zero World Cup fixtures."
        )

    print(f"Fixtures received: {len(fixtures)}")

    return data


def save_raw_data(
    data: dict[str, Any],
    output_file: Path
) -> None:
    """Save the untouched API response to the Raw layer."""

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved raw fixtures data to: {output_file}"
    )


def main() -> None:
    data = fetch_world_cup_fixtures()

    save_raw_data(
        data,
        OUTPUT_FILE
    )

    fixture_count = len(
        data.get("response", [])
    )

    if fixture_count != 104:
        print(
            "Warning: Expected 104 World Cup fixtures, "
            f"but received {fixture_count}."
        )
    else:
        print(
            "Validation passed: "
            "104 World Cup fixtures received."
        )

    print(
        "World Cup fixtures ingestion "
        "completed successfully."
    )


if __name__ == "__main__":
    main()