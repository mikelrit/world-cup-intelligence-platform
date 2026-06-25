import json
from pathlib import Path


STANDINGS_ANALYSIS_FILE = Path("data/silver/standings_analysis/standings_analysis_silver.json")

GOLD_FOLDER = Path("data/gold/team_strength_index")
GOLD_FILE = GOLD_FOLDER / "team_strength_index.json"


def safe_number(value):
    if value is None:
        return 0
    return value


def calculate_team_strength_score(team):
    win_percentage = safe_number(team.get("win_percentage"))
    points_per_match = safe_number(team.get("points_per_match"))
    goals_for_per_match = safe_number(team.get("goals_for_per_match"))
    goals_against_per_match = safe_number(team.get("goals_against_per_match"))
    goals_diff = safe_number(team.get("goals_diff"))

    score = (
        (win_percentage * 0.40) +
        (points_per_match * 10 * 0.25) +
        (goals_diff * 0.20) +
        (goals_for_per_match * 10 * 0.10) -
        (goals_against_per_match * 10 * 0.05)
    )

    return round(score, 2)


def main():
    with open(STANDINGS_ANALYSIS_FILE, "r") as file:
        standings_data = json.load(file)

    gold_teams = []

    for team in standings_data:
        team_strength_score = calculate_team_strength_score(team)

        gold_teams.append({
            "team_id": team.get("team_id"),
            "team_name": team.get("team_name"),
            "league_id": team.get("league_id"),
            "league_name": team.get("league_name"),
            "season": team.get("season"),
            "rank": team.get("rank"),
            "points": team.get("points"),
            "matches_played": team.get("matches_played"),
            "wins": team.get("wins"),
            "draws": team.get("draws"),
            "losses": team.get("losses"),
            "goals_for": team.get("goals_for"),
            "goals_against": team.get("goals_against"),
            "goals_diff": team.get("goals_diff"),
            "win_percentage": team.get("win_percentage"),
            "points_per_match": team.get("points_per_match"),
            "goals_for_per_match": team.get("goals_for_per_match"),
            "goals_against_per_match": team.get("goals_against_per_match"),
            "team_strength_score": team_strength_score
        })

    gold_teams.sort(key=lambda team: team["team_strength_score"], reverse=True)

    for index, team in enumerate(gold_teams, start=1):
        team["strength_rank"] = index

    GOLD_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(GOLD_FILE, "w") as file:
        json.dump(gold_teams, file, indent=4)

    print(f"Gold team strength index file created: {GOLD_FILE}")
    print(f"Records transformed: {len(gold_teams)}")


if __name__ == "__main__":
    main()