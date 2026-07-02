import json
from pathlib import Path


TEAM_STRENGTH_FILE = Path("data/gold/team_strength_index/team_strength_index.json")
PLAYER_DEPENDENCY_FILE = Path("data/gold/player_dependency_score/player_dependency_score.json")

GOLD_FOLDER = Path("data/gold/world_cup_power_rankings")
GOLD_FILE = GOLD_FOLDER / "world_cup_power_rankings.json"


def safe_number(value):
    if value is None:
        return 0

    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def calculate_average(values):
    if len(values) == 0:
        return 0

    return round(sum(values) / len(values), 2)


def main():
    with open(TEAM_STRENGTH_FILE, "r") as file:
        team_strength_data = json.load(file)

    with open(PLAYER_DEPENDENCY_FILE, "r") as file:
        player_dependency_data = json.load(file)

    players_by_team = {}

    for player in player_dependency_data:
        team_id = player.get("team_id")

        if team_id not in players_by_team:
            players_by_team[team_id] = []

        players_by_team[team_id].append(player)

    power_rankings = []

    for team in team_strength_data:
        team_id = team.get("team_id")
        team_players = players_by_team.get(team_id, [])

        dependency_scores = []
        total_goal_contributions = 0
        top_player_name = None
        top_player_dependency_score = 0

        for player in team_players:
            dependency_score = safe_number(player.get("player_dependency_score"))
            goal_contributions = safe_number(player.get("goal_contributions"))

            dependency_scores.append(dependency_score)
            total_goal_contributions += goal_contributions

            if dependency_score > top_player_dependency_score:
                top_player_dependency_score = dependency_score
                top_player_name = player.get("player_name")

        average_player_dependency_score = calculate_average(dependency_scores)
        team_strength_score = safe_number(team.get("team_strength_score"))

        world_cup_power_score = (
            (team_strength_score * 0.70)
            + (average_player_dependency_score * 0.20)
            + (top_player_dependency_score * 0.10)
        )

        power_rankings.append({
            "team_id": team_id,
            "team_name": team.get("team_name"),
            "league_id": team.get("league_id"),
            "league_name": team.get("league_name"),
            "season": team.get("season"),

            "strength_rank": team.get("strength_rank"),
            "team_strength_score": team.get("team_strength_score"),

            "average_player_dependency_score": average_player_dependency_score,
            "top_player_dependency_score": round(top_player_dependency_score, 2),
            "top_player_name": top_player_name,
            "total_goal_contributions": total_goal_contributions,

            "world_cup_power_score": round(world_cup_power_score, 2)
        })

    power_rankings.sort(
        key=lambda team: team["world_cup_power_score"],
        reverse=True
    )

    for index, team in enumerate(power_rankings, start=1):
        team["power_rank"] = index

    GOLD_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(GOLD_FILE, "w") as file:
        json.dump(power_rankings, file, indent=4)

    print(f"Gold World Cup power rankings file created: {GOLD_FILE}")
    print(f"Records transformed: {len(power_rankings)}")


if __name__ == "__main__":
    main()