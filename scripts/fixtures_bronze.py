import json
from pathlib import Path


RAW_FILE = Path("data/raw/fixtures/fixtures.json")
BRONZE_FOLDER = Path("data/bronze/fixtures")
BRONZE_FILE = BRONZE_FOLDER / "fixtures_bronze.json"


def main():
    with open(RAW_FILE, "r") as file:
        raw_data = json.load(file)

    bronze_fixtures = []

    for record in raw_data.get("response", []):
        fixture = record.get("fixture", {})
        league = record.get("league", {})
        teams = record.get("teams", {})
        goals = record.get("goals", {})
        score = record.get("score", {})

        home_team = teams.get("home", {})
        away_team = teams.get("away", {})
        venue = fixture.get("venue", {})
        status = fixture.get("status", {})

        bronze_fixtures.append({
            "fixture_id": fixture.get("id"),
            "fixture_date": fixture.get("date"),
            "timezone": fixture.get("timezone"),
            "status": status.get("long"),
            "status_short": status.get("short"),
            "elapsed": status.get("elapsed"),

            "league_id": league.get("id"),
            "league_name": league.get("name"),
            "season": league.get("season"),
            "round": league.get("round"),

            "venue_id": venue.get("id"),
            "venue_name": venue.get("name"),
            "venue_city": venue.get("city"),

            "home_team_id": home_team.get("id"),
            "home_team_name": home_team.get("name"),
            "home_team_winner": home_team.get("winner"),

            "away_team_id": away_team.get("id"),
            "away_team_name": away_team.get("name"),
            "away_team_winner": away_team.get("winner"),

            "home_goals": goals.get("home"),
            "away_goals": goals.get("away"),

            "home_halftime_goals": score.get("halftime", {}).get("home"),
            "away_halftime_goals": score.get("halftime", {}).get("away"),
            "home_fulltime_goals": score.get("fulltime", {}).get("home"),
            "away_fulltime_goals": score.get("fulltime", {}).get("away"),
        })

    BRONZE_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(BRONZE_FILE, "w") as file:
        json.dump(bronze_fixtures, file, indent=4)

    print(f"Bronze fixtures file created: {BRONZE_FILE}")
    print(f"Records transformed: {len(bronze_fixtures)}")


if __name__ == "__main__":
    main()