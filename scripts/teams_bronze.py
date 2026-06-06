import json
from pathlib import Path


RAW_FILE = Path("data/raw/teams/teams.json")
BRONZE_FOLDER = Path("data/bronze/teams")
BRONZE_FILE = BRONZE_FOLDER / "teams_bronze.json"


def main():
    with open(RAW_FILE, "r") as file:
        raw_data = json.load(file)

    bronze_teams = []

    for record in raw_data.get("response", []):
        team = record.get("team", {})
        venue = record.get("venue", {})

        bronze_teams.append({
            "team_id": team.get("id"),
            "team_name": team.get("name"),
            "team_code": team.get("code"),
            "country": team.get("country"),
            "founded": team.get("founded"),
            "is_national_team": team.get("national"),
            "venue_id": venue.get("id"),
            "venue_name": venue.get("name"),
            "venue_city": venue.get("city"),
            "venue_capacity": venue.get("capacity"),
            "venue_surface": venue.get("surface")
        })

    BRONZE_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(BRONZE_FILE, "w") as file:
        json.dump(bronze_teams, file, indent=4)

    print(f"Bronze teams file created: {BRONZE_FILE}")
    print(f"Records transformed: {len(bronze_teams)}")


if __name__ == "__main__":
    main()