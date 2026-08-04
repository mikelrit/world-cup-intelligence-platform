import json
import os
import time
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
ENDPOINT = "/players"

LEAGUE_ID = 1
SEASON = 2026

HEADERS = {
    "x-apisports-key": API_KEY
}

OUTPUT_FOLDER = Path(
    "data/raw/world_cup/players"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_players_raw.json"
)

REQUEST_DELAY_SECONDS = 1


def request_page(page: int) -> dict[str, Any]:
    """Request one page of World Cup player data."""

    url = f"{BASE_URL}{ENDPOINT}"

    params = {
        "league": LEAGUE_ID,
        "season": SEASON,
        "page": page
    }

    while True:
        print(f"Requesting player page {page}...")

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=60
        )

        if response.status_code == 429:
            retry_after = int(
                response.headers.get("Retry-After", 60)
            )

            print(
                f"Rate limit reached. "
                f"Waiting {retry_after} seconds..."
            )

            time.sleep(retry_after)
            continue

        response.raise_for_status()

        data = response.json()

        api_errors = data.get("errors", {})

        if api_errors:
            raise RuntimeError(
                f"API returned errors on page {page}: {api_errors}"
            )

        return data


def fetch_all_world_cup_players() -> list[dict[str, Any]]:
    """Retrieve every available page of World Cup player data."""

    all_players: list[dict[str, Any]] = []

    current_page = 1
    total_pages = 1

    while current_page <= total_pages:
        data = request_page(current_page)

        page_players = data.get("response", [])
        paging = data.get("paging", {})

        total_pages = paging.get("total", 1)

        all_players.extend(page_players)

        print(
            f"Page {current_page}/{total_pages}: "
            f"{len(page_players)} records received"
        )

        current_page += 1

        if current_page <= total_pages:
            time.sleep(REQUEST_DELAY_SECONDS)

    return all_players


def deduplicate_players(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Remove duplicate player-statistic records.

    A player can appear more than once if the API returns
    multiple team or competition statistic objects.
    """

    unique_records: dict[
        tuple[Any, Any, Any, Any],
        dict[str, Any]
    ] = {}

    for record in records:
        player = record.get("player") or {}
        statistics = record.get("statistics") or []

        if not statistics:
            key = (
                player.get("id"),
                None,
                LEAGUE_ID,
                SEASON
            )
            unique_records[key] = record
            continue

        first_statistic = statistics[0] or {}
        team = first_statistic.get("team") or {}
        league = first_statistic.get("league") or {}

        key = (
            player.get("id"),
            team.get("id"),
            league.get("id"),
            league.get("season")
        )

        unique_records[key] = record

    return list(unique_records.values())


def save_raw_data(
    players: list[dict[str, Any]]
) -> None:
    """Save all collected player data into the Raw layer."""

    output_data = {
        "get": "players",
        "parameters": {
            "league": str(LEAGUE_ID),
            "season": str(SEASON)
        },
        "errors": [],
        "results": len(players),
        "paging": {
            "current": 1,
            "total": 1
        },
        "response": players
    }

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            output_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved raw player data to: {OUTPUT_FILE}")


def main() -> None:
    players = fetch_all_world_cup_players()

    if not players:
        raise RuntimeError(
            "The API returned zero World Cup player records."
        )

    print(f"Player records collected: {len(players)}")

    players = deduplicate_players(players)

    print(
        f"Player records after deduplication: {len(players)}"
    )

    save_raw_data(players)

    print(
        "World Cup players ingestion completed successfully."
    )


if __name__ == "__main__":
    main()
