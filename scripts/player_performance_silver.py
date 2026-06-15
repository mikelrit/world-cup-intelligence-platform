import json
from pathlib import Path


PLAYERS_BRONZE_FILE = Path("data/bronze/players/players_bronze.json")

SILVER_FOLDER = Path("data/silver/player_performance")
SILVER_FILE = SILVER_FOLDER / "player_performance_silver.json"


def safe_divide(numerator, denominator):
    if denominator is None or denominator == 0:
        return None

    if numerator is None:
        return None

    return round(numerator / denominator, 2)


def main():
    with open(PLAYERS_BRONZE_FILE, "r") as file:
        players_data = json.load(file)

    silver_players = []

    for player in players_data:
        minutes = player.get("minutes")
        goals = player.get("goals_total")
        assists = player.get("goals_assists")
        shots = player.get("shots_total")
        shots_on_target = player.get("shots_on_target")
        passes_total = player.get("passes_total")
        passes_key = player.get("passes_key")
        duels_total = player.get("duels_total")
        duels_won = player.get("duels_won")
        dribbles_attempts = player.get("dribbles_attempts")
        dribbles_success = player.get("dribbles_success")

        silver_players.append({
            "player_id": player.get("player_id"),
            "player_name": player.get("player_name"),
            "age": player.get("age"),
            "nationality": player.get("nationality"),
            "position": player.get("position"),

            "team_id": player.get("team_id"),
            "team_name": player.get("team_name"),
            "league_id": player.get("league_id"),
            "league_name": player.get("league_name"),
            "season": player.get("season"),

            "appearances": player.get("appearances"),
            "lineups": player.get("lineups"),
            "minutes": minutes,
            "rating": player.get("rating"),
            "captain": player.get("captain"),
            "injured": player.get("injured"),

            "goals_total": goals,
            "goals_assists": assists,
            "shots_total": shots,
            "shots_on_target": shots_on_target,
            "passes_total": passes_total,
            "passes_key": passes_key,
            "duels_total": duels_total,
            "duels_won": duels_won,
            "dribbles_attempts": dribbles_attempts,
            "dribbles_success": dribbles_success,
            "yellow_cards": player.get("yellow_cards"),
            "red_cards": player.get("red_cards"),

            "goal_contributions": (goals or 0) + (assists or 0),
            "goals_per_90": safe_divide((goals or 0) * 90, minutes),
            "assists_per_90": safe_divide((assists or 0) * 90, minutes),
            "shots_on_target_rate": safe_divide(shots_on_target, shots),
            "key_pass_rate": safe_divide(passes_key, passes_total),
            "duel_success_rate": safe_divide(duels_won, duels_total),
            "dribble_success_rate": safe_divide(dribbles_success, dribbles_attempts)
        })

    SILVER_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(SILVER_FILE, "w") as file:
        json.dump(silver_players, file, indent=4)

    print(f"Silver player performance file created: {SILVER_FILE}")
    print(f"Records transformed: {len(silver_players)}")


if __name__ == "__main__":
    main()