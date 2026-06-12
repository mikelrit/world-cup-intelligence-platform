import json
from pathlib import Path


TEAMS_BRONZE_FILE = Path("data/bronze/teams/teams_bronze.json")
STANDINGS_BRONZE_FILE = Path("data/bronze/standings/standings_bronze.json")

SILVER_FOLDER = Path("data/silver/team_performance")
SILVER_FILE = SILVER_FOLDER / "team_performance_silver.json"


def safe_divide(numerator, denominator):
    if denominator is None or denominator == 0:
        return None

    if numerator is None:
        return None

    return round(numerator / denominator, 2)


def main():
    with open(TEAMS_BRONZE_FILE, "r") as file:
        teams_data = json.load(file)

    with open(STANDINGS_BRONZE_FILE, "r") as file:
        standings_data = json.load(file)

    teams_lookup = {}

    for team in teams_data:
        team_id = team.get("team_id")
        teams_lookup[team_id] = team

    silver_team_performance = []

    for standing in standings_data:
        team_id = standing.get("team_id")
        team_info = teams_lookup.get(team_id, {})

        matches_played = standing.get("matches_played")
        wins = standing.get("wins")
        points = standing.get("points")

        win_percentage = safe_divide(wins * 100 if wins is not None else None, matches_played)
        points_per_match = safe_divide(points, matches_played)

        silver_team_performance.append({
            "team_id": team_id,
            "team_name": standing.get("team_name") or team_info.get("team_name"),
            "country": team_info.get("country"),

            "league_id": standing.get("league_id"),
            "league_name": standing.get("league_name"),
            "season": standing.get("season"),

            "rank": standing.get("rank"),
            "points": points,
            "matches_played": matches_played,
            "wins": wins,
            "draws": standing.get("draws"),
            "losses": standing.get("losses"),

            "goals_for": standing.get("goals_for"),
            "goals_against": standing.get("goals_against"),
            "goals_diff": standing.get("goals_diff"),
            "form": standing.get("form"),

            "win_percentage": win_percentage,
            "points_per_match": points_per_match,

            "venue_name": team_info.get("venue_name"),
            "venue_city": team_info.get("venue_city")
        })

    SILVER_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(SILVER_FILE, "w") as file:
        json.dump(silver_team_performance, file, indent=4)

    print(f"Silver team performance file created: {SILVER_FILE}")
    print(f"Records transformed: {len(silver_team_performance)}")


if __name__ == "__main__":
    main()