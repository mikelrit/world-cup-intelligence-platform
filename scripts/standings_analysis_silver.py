import json
from pathlib import Path


STANDINGS_BRONZE_FILE = Path("data/bronze/standings/standings_bronze.json")

SILVER_FOLDER = Path("data/silver/standings_analysis")
SILVER_FILE = SILVER_FOLDER / "standings_analysis_silver.json"


def safe_divide(numerator, denominator):
    if denominator is None or denominator == 0:
        return None

    if numerator is None:
        return None

    return round(numerator / denominator, 2)


def main():
    with open(STANDINGS_BRONZE_FILE, "r") as file:
        standings_data = json.load(file)

    silver_standings = []

    for team in standings_data:
        matches_played = team.get("matches_played")
        wins = team.get("wins")
        points = team.get("points")
        goals_for = team.get("goals_for")
        goals_against = team.get("goals_against")

        silver_standings.append({
            "league_id": team.get("league_id"),
            "league_name": team.get("league_name"),
            "season": team.get("season"),
            "country": team.get("country"),

            "team_id": team.get("team_id"),
            "team_name": team.get("team_name"),
            "rank": team.get("rank"),
            "group": team.get("group"),

            "points": points,
            "matches_played": matches_played,
            "wins": wins,
            "draws": team.get("draws"),
            "losses": team.get("losses"),

            "goals_for": goals_for,
            "goals_against": goals_against,
            "goals_diff": team.get("goals_diff"),
            "form": team.get("form"),

            "win_percentage": safe_divide((wins or 0) * 100, matches_played),
            "points_per_match": safe_divide(points, matches_played),
            "goals_for_per_match": safe_divide(goals_for, matches_played),
            "goals_against_per_match": safe_divide(goals_against, matches_played)
        })

    SILVER_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(SILVER_FILE, "w") as file:
        json.dump(silver_standings, file, indent=4)

    print(f"Silver standings analysis file created: {SILVER_FILE}")
    print(f"Records transformed: {len(silver_standings)}")


if __name__ == "__main__":
    main()