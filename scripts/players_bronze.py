import json
from pathlib import Path


RAW_FILE = Path("data/raw/players/players.json")
BRONZE_FOLDER = Path("data/bronze/players")
BRONZE_FILE = BRONZE_FOLDER / "players_bronze.json"


def main():
    with open(RAW_FILE, "r") as file:
        raw_data = json.load(file)

    bronze_players = []

    for record in raw_data.get("response", []):
        player = record.get("player", {})
        statistics_list = record.get("statistics", [])

        for stat in statistics_list:
            team = stat.get("team", {})
            league = stat.get("league", {})
            games = stat.get("games", {})
            goals = stat.get("goals", {})
            passes = stat.get("passes", {})
            shots = stat.get("shots", {})
            dribbles = stat.get("dribbles", {})
            duels = stat.get("duels", {})
            tackles = stat.get("tackles", {})
            cards = stat.get("cards", {})

            bronze_players.append({
                "player_id": player.get("id"),
                "player_name": player.get("name"),
                "firstname": player.get("firstname"),
                "lastname": player.get("lastname"),
                "age": player.get("age"),
                "birth_date": player.get("birth", {}).get("date"),
                "birth_place": player.get("birth", {}).get("place"),
                "birth_country": player.get("birth", {}).get("country"),
                "nationality": player.get("nationality"),
                "height": player.get("height"),
                "weight": player.get("weight"),
                "injured": player.get("injured"),

                "team_id": team.get("id"),
                "team_name": team.get("name"),
                "league_id": league.get("id"),
                "league_name": league.get("name"),
                "season": league.get("season"),

                "appearances": games.get("appearences"),
                "lineups": games.get("lineups"),
                "minutes": games.get("minutes"),
                "position": games.get("position"),
                "rating": games.get("rating"),
                "captain": games.get("captain"),

                "goals_total": goals.get("total"),
                "goals_assists": goals.get("assists"),
                "shots_total": shots.get("total"),
                "shots_on_target": shots.get("on"),

                "passes_total": passes.get("total"),
                "passes_key": passes.get("key"),
                "passes_accuracy": passes.get("accuracy"),

                "dribbles_attempts": dribbles.get("attempts"),
                "dribbles_success": dribbles.get("success"),

                "duels_total": duels.get("total"),
                "duels_won": duels.get("won"),

                "tackles_total": tackles.get("total"),
                "blocks": tackles.get("blocks"),
                "interceptions": tackles.get("interceptions"),

                "yellow_cards": cards.get("yellow"),
                "red_cards": cards.get("red")
            })

    BRONZE_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(BRONZE_FILE, "w") as file:
        json.dump(bronze_players, file, indent=4)

    print(f"Bronze players file created: {BRONZE_FILE}")
    print(f"Records transformed: {len(bronze_players)}")


if __name__ == "__main__":
    main()