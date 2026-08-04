import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/bronze/world_cup/players/"
    "world_cup_players_bronze.json"
)

OUTPUT_FOLDER = Path(
    "data/silver/world_cup/player_performance"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_player_performance_silver.json"
)


def load_json(file_path: Path) -> list[dict[str, Any]]:
    """Load and validate the Bronze players file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Bronze players file was not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise TypeError(
            f"Expected a list in {file_path}, "
            f"but received {type(data).__name__}."
        )

    return data


def safe_number(value: Any) -> float:
    """Convert a value to a float safely."""

    if value is None:
        return 0.0

    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_average(
    numerator: Any,
    denominator: Any
) -> float:
    """Calculate an average safely."""

    numerator_value = safe_number(numerator)
    denominator_value = safe_number(denominator)

    if denominator_value == 0:
        return 0.0

    return round(
        numerator_value / denominator_value,
        2
    )


def safe_percentage(
    numerator: Any,
    denominator: Any
) -> float:
    """Calculate a percentage safely."""

    numerator_value = safe_number(numerator)
    denominator_value = safe_number(denominator)

    if denominator_value == 0:
        return 0.0

    return round(
        numerator_value / denominator_value * 100,
        2
    )


def calculate_per_90(
    value: Any,
    minutes: Any
) -> float:
    """Calculate a per-90-minute rate."""

    value_number = safe_number(value)
    minutes_number = safe_number(minutes)

    if minutes_number == 0:
        return 0.0

    return round(
        value_number / minutes_number * 90,
        2
    )


def normalize_rating(value: Any) -> float:
    """Convert the API rating into a clean decimal."""

    rating = safe_number(value)

    if rating < 0:
        return 0.0

    return round(rating, 2)


def transform_player(
    player: dict[str, Any]
) -> dict[str, Any]:
    """Create one Silver-layer player performance record."""

    appearances = int(
        safe_number(
            player.get("appearances")
        )
    )

    lineups = int(
        safe_number(
            player.get("lineups")
        )
    )

    minutes = int(
        safe_number(
            player.get("minutes")
        )
    )

    goals_total = int(
        safe_number(
            player.get("goals_total")
        )
    )

    goals_assists = int(
        safe_number(
            player.get("goals_assists")
        )
    )

    shots_total = int(
        safe_number(
            player.get("shots_total")
        )
    )

    shots_on_target = int(
        safe_number(
            player.get("shots_on_target")
        )
    )

    passes_total = int(
        safe_number(
            player.get("passes_total")
        )
    )

    passes_key = int(
        safe_number(
            player.get("passes_key")
        )
    )

    duels_total = int(
        safe_number(
            player.get("duels_total")
        )
    )

    duels_won = int(
        safe_number(
            player.get("duels_won")
        )
    )

    dribbles_attempts = int(
        safe_number(
            player.get("dribbles_attempts")
        )
    )

    dribbles_success = int(
        safe_number(
            player.get("dribbles_success")
        )
    )

    tackles_total = int(
        safe_number(
            player.get("tackles_total")
        )
    )

    interceptions = int(
        safe_number(
            player.get("interceptions")
        )
    )

    fouls_drawn = int(
        safe_number(
            player.get("fouls_drawn")
        )
    )

    fouls_committed = int(
        safe_number(
            player.get("fouls_committed")
        )
    )

    yellow_cards = int(
        safe_number(
            player.get("yellow_cards")
        )
    )

    red_cards = int(
        safe_number(
            player.get("red_cards")
        )
    )

    goal_contributions = (
        goals_total + goals_assists
    )

    return {
        "player_id": player.get("player_id"),
        "player_name": player.get("player_name"),
        "first_name": player.get("first_name"),
        "last_name": player.get("last_name"),
        "age": player.get("age"),
        "nationality": player.get("nationality"),
        "position": player.get("position"),
        "injured": player.get("injured"),
        "player_photo": player.get("player_photo"),

        "team_id": player.get("team_id"),
        "team_name": player.get("team_name"),
        "team_logo": player.get("team_logo"),

        "league_id": player.get("league_id"),
        "league_name": player.get("league_name"),
        "season": player.get("season"),

        "appearances": appearances,
        "lineups": lineups,
        "minutes": minutes,
        "rating": normalize_rating(
            player.get("rating")
        ),

        "goals_total": goals_total,
        "goals_assists": goals_assists,
        "goal_contributions": goal_contributions,

        "goals_per_90": calculate_per_90(
            goals_total,
            minutes
        ),
        "assists_per_90": calculate_per_90(
            goals_assists,
            minutes
        ),
        "goal_contributions_per_90": calculate_per_90(
            goal_contributions,
            minutes
        ),

        "shots_total": shots_total,
        "shots_on_target": shots_on_target,
        "shots_on_target_rate": safe_percentage(
            shots_on_target,
            shots_total
        ),

        "passes_total": passes_total,
        "passes_key": passes_key,
        "pass_accuracy": safe_number(
            player.get("passes_accuracy")
        ),
        "key_pass_rate": safe_percentage(
            passes_key,
            passes_total
        ),

        "tackles_total": tackles_total,
        "blocks": int(
            safe_number(
                player.get("blocks")
            )
        ),
        "interceptions": interceptions,
        "defensive_actions": (
            tackles_total
            + interceptions
            + int(
                safe_number(
                    player.get("blocks")
                )
            )
        ),

        "duels_total": duels_total,
        "duels_won": duels_won,
        "duel_success_rate": safe_percentage(
            duels_won,
            duels_total
        ),

        "dribbles_attempts": dribbles_attempts,
        "dribbles_success": dribbles_success,
        "dribble_success_rate": safe_percentage(
            dribbles_success,
            dribbles_attempts
        ),

        "fouls_drawn": fouls_drawn,
        "fouls_committed": fouls_committed,

        "yellow_cards": yellow_cards,
        "red_cards": red_cards,

        "penalties_scored": int(
            safe_number(
                player.get("penalties_scored")
            )
        ),
        "penalties_missed": int(
            safe_number(
                player.get("penalties_missed")
            )
        ),
        "penalties_saved": int(
            safe_number(
                player.get("penalties_saved")
            )
        )
    }


def validate_record(record: dict[str, Any]) -> None:
    """Validate required Silver player fields."""

    required_fields = [
        "player_id",
        "player_name",
        "team_id",
        "team_name",
        "league_id",
        "season"
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Player performance record is missing "
            f"{missing_fields}: {record}"
        )


def remove_duplicates(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Remove duplicate player-team-season records."""

    unique_records: dict[
        tuple[Any, Any, Any, Any],
        dict[str, Any]
    ] = {}

    for record in records:
        key = (
            record["player_id"],
            record["team_id"],
            record["league_id"],
            record["season"]
        )

        unique_records[key] = record

    return list(unique_records.values())


def save_silver_data(
    records: list[dict[str, Any]]
) -> None:
    """Save the Silver player-performance dataset."""

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Silver player performance file created: "
        f"{OUTPUT_FILE}"
    )


def main() -> None:
    players = load_json(INPUT_FILE)

    if not players:
        raise RuntimeError(
            "The Bronze players file is empty."
        )

    silver_records = []

    for player in players:
        record = transform_player(player)
        validate_record(record)
        silver_records.append(record)

    silver_records = remove_duplicates(silver_records)

    silver_records.sort(
        key=lambda record: (
            record["team_name"],
            -record["goal_contributions"],
            -record["rating"],
            record["player_name"]
        )
    )

    save_silver_data(silver_records)

    team_ids = {
        record["team_id"]
        for record in silver_records
    }

    players_with_minutes = sum(
        1
        for record in silver_records
        if record["minutes"] > 0
    )

    players_with_contributions = sum(
        1
        for record in silver_records
        if record["goal_contributions"] > 0
    )

    print(f"Bronze player records loaded: {len(players)}")
    print(f"National teams represented: {len(team_ids)}")
    print(f"Silver player records created: {len(silver_records)}")
    print(f"Players with recorded minutes: {players_with_minutes}")
    print(
        f"Players with goal contributions: "
        f"{players_with_contributions}"
    )

    if len(team_ids) != 48:
        print(
            "Warning: Expected 48 national teams, "
            f"but found {len(team_ids)}."
        )
    else:
        print(
            "Validation passed: player data covers "
            "all 48 World Cup teams."
        )

    print(
        "World Cup player performance "
        "Silver transformation completed."
    )


if __name__ == "__main__":
    main()
