import json
from pathlib import Path


PLAYER_PERFORMANCE_FILE = Path("data/silver/player_performance/player_performance_silver.json")

GOLD_FOLDER = Path("data/gold/player_dependency_score")
GOLD_FILE = GOLD_FOLDER / "player_dependency_score.json"


def safe_number(value):
    if value is None:
        return 0

    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def calculate_dependency_score(player):
    goal_contributions = safe_number(player.get("goal_contributions"))
    goals_per_90 = safe_number(player.get("goals_per_90"))
    assists_per_90 = safe_number(player.get("assists_per_90"))
    rating = safe_number(player.get("rating"))
    duel_success_rate = safe_number(player.get("duel_success_rate"))
    dribble_success_rate = safe_number(player.get("dribble_success_rate"))
    key_pass_rate = safe_number(player.get("key_pass_rate"))

    score = (
        (goal_contributions * 3)
        + (goals_per_90 * 20)
        + (assists_per_90 * 20)
        + (rating * 5)
        + (duel_success_rate * 10)
        + (dribble_success_rate * 10)
        + (key_pass_rate * 10)
    )

    if player.get("injured") is True:
        score -= 10

    return round(score, 2)


def main():
    with open(PLAYER_PERFORMANCE_FILE, "r") as file:
        players_data = json.load(file)

    gold_players = []

    for player in players_data:
        dependency_score = calculate_dependency_score(player)

        gold_players.append({
            "player_id": player.get("player_id"),
            "player_name": player.get("player_name"),
            "team_id": player.get("team_id"),
            "team_name": player.get("team_name"),
            "league_id": player.get("league_id"),
            "league_name": player.get("league_name"),
            "season": player.get("season"),
            "position": player.get("position"),
            "appearances": player.get("appearances"),
            "minutes": player.get("minutes"),
            "rating": player.get("rating"),
            "injured": player.get("injured"),

            "goals_total": player.get("goals_total"),
            "goals_assists": player.get("goals_assists"),
            "goal_contributions": player.get("goal_contributions"),
            "goals_per_90": player.get("goals_per_90"),
            "assists_per_90": player.get("assists_per_90"),
            "shots_on_target_rate": player.get("shots_on_target_rate"),
            "key_pass_rate": player.get("key_pass_rate"),
            "duel_success_rate": player.get("duel_success_rate"),
            "dribble_success_rate": player.get("dribble_success_rate"),

            "player_dependency_score": dependency_score
        })

    gold_players.sort(key=lambda player: player["player_dependency_score"], reverse=True)

    for index, player in enumerate(gold_players, start=1):
        player["dependency_rank"] = index

    GOLD_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(GOLD_FILE, "w") as file:
        json.dump(gold_players, file, indent=4)

    print(f"Gold player dependency score file created: {GOLD_FILE}")
    print(f"Records transformed: {len(gold_players)}")


if __name__ == "__main__":
    main()