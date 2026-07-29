import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise ValueError("API_FOOTBALL_KEY was not found in the .env file.")

URL = "https://v3.football.api-sports.io/players"

HEADERS = {
    "x-apisports-key": API_KEY
}

SEASON = 2023

TEAM_STRENGTH_FILE = Path(
    "data/gold/team_strength_index/team_strength_index.json"
)

OUTPUT_FOLDER = Path("data/raw/players")
OUTPUT_FILE = OUTPUT_FOLDER / "players.json"

REQUEST_DELAY_SECONDS = 7
RATE_LIMIT_WAIT_SECONDS = 60
MAX_FREE_PLAN_PAGES = 3


def load_team_ids():
    with open(TEAM_STRENGTH_FILE, "r", encoding="utf-8") as file:
        teams = json.load(file)

    team_ids = sorted({
        team.get("team_id")
        for team in teams
        if team.get("team_id") is not None
    })

    if not team_ids:
        raise ValueError("No team IDs were found in the team strength file.")

    return team_ids


def request_page(team_id, page):
    params = {
        "team": team_id,
        "season": SEASON,
        "page": page
    }

    while True:
        response = requests.get(
            URL,
            headers=HEADERS,
            params=params,
            timeout=30
        )

        if response.status_code == 429:
            print(
                f"Rate limit reached for team {team_id}, page {page}. "
                f"Waiting {RATE_LIMIT_WAIT_SECONDS} seconds..."
            )
            time.sleep(RATE_LIMIT_WAIT_SECONDS)
            continue

        response.raise_for_status()

        data = response.json()
        api_errors = data.get("errors", {})

        if api_errors:
            raise RuntimeError(
                f"API returned errors for team {team_id}, "
                f"page {page}: {api_errors}"
            )

        return data


def fetch_players_for_team(team_id):
    team_players = []
    current_page = 1
    total_pages = 1

    while (
        current_page <= total_pages
        and current_page <= MAX_FREE_PLAN_PAGES
    ):
        print(f"Team {team_id}: requesting page {current_page}...")

        data = request_page(team_id, current_page)

        page_players = data.get("response", [])
        team_players.extend(page_players)

        paging = data.get("paging", {})
        total_pages = paging.get("total", 1)

        print(
            f"Team {team_id}: page {current_page}/{total_pages}, "
            f"{len(page_players)} players received"
        )

        current_page += 1

        time.sleep(REQUEST_DELAY_SECONDS)

    if total_pages > MAX_FREE_PLAN_PAGES:
        print(
            f"Team {team_id}: free plan limited collection to "
            f"{MAX_FREE_PLAN_PAGES} of {total_pages} pages."
        )

    return team_players


def deduplicate_players(players):
    unique_players = {}

    for record in players:
        player = record.get("player", {})
        statistics = record.get("statistics", [])

        player_id = player.get("id")

        team_id = None
        league_id = None
        season = None

        if statistics:
            first_stat = statistics[0]

            team_id = first_stat.get("team", {}).get("id")
            league_id = first_stat.get("league", {}).get("id")
            season = first_stat.get("league", {}).get("season")

        key = (
            player_id,
            team_id,
            league_id,
            season
        )

        unique_players[key] = record

    return list(unique_players.values())


def main():
    team_ids = load_team_ids()
    all_players = []

    print(f"Collecting players for {len(team_ids)} teams.")

    for team_id in team_ids:
        try:
            team_players = fetch_players_for_team(team_id)
            all_players.extend(team_players)

        except requests.RequestException as error:
            print(f"Request failed for team {team_id}: {error}")

        except RuntimeError as error:
            print(error)

    all_players = deduplicate_players(all_players)

    if not all_players:
        raise ValueError("No player records were collected.")

    output_data = {
        "get": "players",
        "parameters": {
            "season": SEASON,
            "team_ids": team_ids
        },
        "errors": [],
        "results": len(all_players),
        "paging": {
            "current": 1,
            "total": 1
        },
        "response": all_players
    }

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4)

    print()
    print(f"Saved {len(all_players)} player records to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()