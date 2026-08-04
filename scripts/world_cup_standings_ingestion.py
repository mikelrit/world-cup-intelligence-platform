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
ENDPOINT = "/standings"

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
    "data/raw/world_cup/standings"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_standings_raw.json"
)


def fetch_world_cup_standings() -> dict[str, Any]:
    """Retrieve the 2026 FIFA World Cup group standings."""

    url = f"{BASE_URL}{ENDPOINT}"

    print("Requesting 2026 World Cup standings...")

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

    standings_response = data.get("response", [])

    if not standings_response:
        raise RuntimeError(
            "The API returned zero World Cup standings records."
        )

    return data


def count_groups(data: dict[str, Any]) -> int:
    """Count the group tables contained inside the nested response."""

    responses = data.get("response", [])

    if not responses:
        return 0

    league = responses[0].get("league") or {}
    standings = league.get("standings") or []

    return len(standings)


def count_team_rows(data: dict[str, Any]) -> int:
    """Count all team rows across every World Cup group."""

    responses = data.get("response", [])

    if not responses:
        return 0

    league = responses[0].get("league") or {}
    standings = league.get("standings") or []

    return sum(len(group) for group in standings)


def save_raw_data(
    data: dict[str, Any],
    output_file: Path
) -> None:
    """Save the untouched standings response to the Raw layer."""

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

    print(f"Saved raw standings data to: {output_file}")


def main() -> None:
    data = fetch_world_cup_standings()

    group_count = count_groups(data)
    team_row_count = count_team_rows(data)

    print(f"Groups received: {group_count}")
    print(f"Standing team rows received: {team_row_count}")

    save_raw_data(
        data,
        OUTPUT_FILE
    )

    if group_count != 12:
        print(
            "Warning: Expected 12 World Cup groups, "
            f"but found {group_count}."
        )
    else:
        print("Validation passed: 12 World Cup groups found.")

    if team_row_count != 48:
        print(
            "Warning: Expected 48 standing team rows, "
            f"but found {team_row_count}."
        )
    else:
        print(
            "Validation passed: "
            "48 World Cup standing team rows found."
        )

    print(
        "World Cup standings ingestion "
        "completed successfully."
    )


if __name__ == "__main__":
    main()