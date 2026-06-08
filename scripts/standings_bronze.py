import json
from pathlib import Path


RAW_FILE = Path("data/raw/standings/standings.json")
BRONZE_FOLDER = Path("data/bronze/standings")
BRONZE_FILE = BRONZE_FOLDER / "standings_bronze.json"


def main():
    with open(RAW_FILE, "r") as file:
        raw_data = json.load(file)

    bronze_standings = []

    for league_record in raw_data.get("response", []):
        league = league_record.get("league", {})
        league_id = league.get("id")
        league_name = league.get("name")
        season = league.get("season")
        country = league.get("country")

        standings_groups = league.get("standings", [])

        for group in standings_groups:
            for team_record in group:
                team = team_record.get("team", {})
                all_stats = team_record.get("all", {})
                home_stats = team_record.get("home", {})
                away_stats = team_record.get("away", {})
                goals_for = all_stats.get("goals", {}).get("for")
                goals_against = all_stats.get("goals", {}).get("against")

                bronze_standings.append({
                    "league_id": league_id,
                    "league_name": league_name,
                    "season": season,
                    "country": country,

                    "rank": team_record.get("rank"),
                    "team_id": team.get("id"),
                    "team_name": team.get("name"),
                    "group": team_record.get("group"),
                    "points": team_record.get("points"),
                    "goals_diff": team_record.get("goalsDiff"),
                    "form": team_record.get("form"),
                    "status": team_record.get("status"),
                    "description": team_record.get("description"),

                    "matches_played": all_stats.get("played"),
                    "wins": all_stats.get("win"),
                    "draws": all_stats.get("draw"),
                    "losses": all_stats.get("lose"),
                    "goals_for": goals_for,
                    "goals_against": goals_against,

                    "home_matches_played": home_stats.get("played"),
                    "home_wins": home_stats.get("win"),
                    "home_draws": home_stats.get("draw"),
                    "home_losses": home_stats.get("lose"),

                    "away_matches_played": away_stats.get("played"),
                    "away_wins": away_stats.get("win"),
                    "away_draws": away_stats.get("draw"),
                    "away_losses": away_stats.get("lose")
                })

    BRONZE_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(BRONZE_FILE, "w") as file:
        json.dump(bronze_standings, file, indent=4)

    print(f"Bronze standings file created: {BRONZE_FILE}")
    print(f"Records transformed: {len(bronze_standings)}")


if __name__ == "__main__":
    main()