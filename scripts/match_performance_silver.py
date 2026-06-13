import json
from pathlib import Path


FIXTURES_BRONZE_FILE = Path("data/bronze/fixtures/fixtures_bronze.json")

SILVER_FOLDER = Path("data/silver/match_performance")
SILVER_FILE = SILVER_FOLDER / "match_performance_silver.json"


def determine_winner(home_team_name, away_team_name, home_goals, away_goals):
    if home_goals is None or away_goals is None:
        return None

    if home_goals > away_goals:
        return home_team_name

    if away_goals > home_goals:
        return away_team_name

    return "Draw"


def main():
    with open(FIXTURES_BRONZE_FILE, "r") as file:
        fixtures_data = json.load(file)

    silver_matches = []

    for fixture in fixtures_data:
        home_goals = fixture.get("home_goals")
        away_goals = fixture.get("away_goals")

        total_goals = None
        goal_difference = None

        if home_goals is not None and away_goals is not None:
            total_goals = home_goals + away_goals
            goal_difference = abs(home_goals - away_goals)

        winner = determine_winner(
            fixture.get("home_team_name"),
            fixture.get("away_team_name"),
            home_goals,
            away_goals
        )

        silver_matches.append({
            "fixture_id": fixture.get("fixture_id"),
            "fixture_date": fixture.get("fixture_date"),
            "status": fixture.get("status"),
            "status_short": fixture.get("status_short"),

            "league_id": fixture.get("league_id"),
            "league_name": fixture.get("league_name"),
            "season": fixture.get("season"),
            "round": fixture.get("round"),

            "venue_name": fixture.get("venue_name"),
            "venue_city": fixture.get("venue_city"),

            "home_team_id": fixture.get("home_team_id"),
            "home_team_name": fixture.get("home_team_name"),
            "away_team_id": fixture.get("away_team_id"),
            "away_team_name": fixture.get("away_team_name"),

            "home_goals": home_goals,
            "away_goals": away_goals,

            "winner": winner,
            "total_goals": total_goals,
            "goal_difference": goal_difference
        })

    SILVER_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(SILVER_FILE, "w") as file:
        json.dump(silver_matches, file, indent=4)

    print(f"Silver match performance file created: {SILVER_FILE}")
    print(f"Records transformed: {len(silver_matches)}")


if __name__ == "__main__":
    main()