import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/raw/world_cup/players/world_cup_players_raw.json"
)

OUTPUT_FOLDER = Path(
    "data/bronze/world_cup/players"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_players_bronze.json"
)


def load_raw_data(file_path: Path) -> dict[str, Any]:
    """Load the combined World Cup players Raw file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw players file was not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    api_errors = data.get("errors", {})

    if api_errors:
        raise RuntimeError(
            f"Raw API file contains errors: {api_errors}"
        )

    return data


def safe_percentage(
    successful: Any,
    attempts: Any
) -> float:
    """Calculate a percentage safely."""

    try:
        successful_value = float(successful or 0)
        attempts_value = float(attempts or 0)

        if attempts_value == 0:
            return 0.0

        return round(
            successful_value / attempts_value * 100,
            2
        )

    except (TypeError, ValueError):
        return 0.0


def transform_player_record(
    record: dict[str, Any],
    statistic: dict[str, Any]
) -> dict[str, Any]:
    """Flatten one player-statistics record."""

    player = record.get("player") or {}

    birth = player.get("birth") or {}

    team = statistic.get("team") or {}
    league = statistic.get("league") or {}
    games = statistic.get("games") or {}
    substitutes = statistic.get("substitutes") or {}
    shots = statistic.get("shots") or {}
    goals = statistic.get("goals") or {}
    passes = statistic.get("passes") or {}
    tackles = statistic.get("tackles") or {}
    duels = statistic.get("duels") or {}
    dribbles = statistic.get("dribbles") or {}
    fouls = statistic.get("fouls") or {}
    cards = statistic.get("cards") or {}
    penalty = statistic.get("penalty") or {}

    return {
        "player_id": player.get("id"),
        "player_name": player.get("name"),
        "first_name": player.get("firstname"),
        "last_name": player.get("lastname"),
        "age": player.get("age"),
        "birth_date": birth.get("date"),
        "birth_place": birth.get("place"),
        "birth_country": birth.get("country"),
        "nationality": player.get("nationality"),
        "height": player.get("height"),
        "weight": player.get("weight"),
        "injured": player.get("injured"),
        "player_photo": player.get("photo"),

        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "team_logo": team.get("logo"),

        "league_id": league.get("id"),
        "league_name": league.get("name"),
        "league_country": league.get("country"),
        "league_logo": league.get("logo"),
        "league_flag": league.get("flag"),
        "season": league.get("season"),

        "appearances": games.get("appearences"),
        "lineups": games.get("lineups"),
        "minutes": games.get("minutes"),
        "position": games.get("position"),
        "rating": games.get("rating"),
        "captain": games.get("captain"),

        "substitutes_in": substitutes.get("in"),
        "substitutes_out": substitutes.get("out"),
        "substitutes_bench": substitutes.get("bench"),

        "shots_total": shots.get("total"),
        "shots_on_target": shots.get("on"),

        "goals_total": goals.get("total"),
        "goals_conceded": goals.get("conceded"),
        "goals_assists": goals.get("assists"),
        "goals_saves": goals.get("saves"),

        "passes_total": passes.get("total"),
        "passes_key": passes.get("key"),
        "passes_accuracy": passes.get("accuracy"),

        "tackles_total": tackles.get("total"),
        "blocks": tackles.get("blocks"),
        "interceptions": tackles.get("interceptions"),

        "duels_total": duels.get("total"),
        "duels_won": duels.get("won"),
        "duel_success_rate": safe_percentage(
            duels.get("won"),
            duels.get("total")
        ),

        "dribbles_attempts": dribbles.get("attempts"),
        "dribbles_success": dribbles.get("success"),
        "dribbles_past": dribbles.get("past"),
        "dribble_success_rate": safe_percentage(
            dribbles.get("success"),
            dribbles.get("attempts")
        ),

        "fouls_drawn": fouls.get("drawn"),
        "fouls_committed": fouls.get("committed"),

        "yellow_cards": cards.get("yellow"),
        "second_yellow_cards": cards.get("yellowred"),
        "red_cards": cards.get("red"),

        "penalties_won": penalty.get("won"),
        "penalties_committed": penalty.get("commited"),
        "penalties_scored": penalty.get("scored"),
        "penalties_missed": penalty.get("missed"),
        "penalties_saved": penalty.get("saved")
    }


def validate_player_record(
    record: dict[str, Any]
) -> None:
    """Validate required Bronze-layer fields."""

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
            f"Player record is missing required fields "
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


def save_bronze_data(
    records: list[dict[str, Any]],
    output_file: Path
) -> None:
    """Save flattened World Cup player records."""

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Bronze players file created: {output_file}")


def main() -> None:
    raw_data = load_raw_data(INPUT_FILE)

    raw_records = raw_data.get("response", [])

    if not raw_records:
        raise RuntimeError(
            "No World Cup player records were found "
            "in the Raw file."
        )

    bronze_records: list[dict[str, Any]] = []
    skipped_records = 0

    for raw_record in raw_records:
        statistics = raw_record.get("statistics") or []

        if not statistics:
            skipped_records += 1
            continue

        for statistic in statistics:
            bronze_record = transform_player_record(
                raw_record,
                statistic
            )

            if (
                bronze_record.get("league_id") != 1
                or bronze_record.get("season") != 2026
            ):
                continue

            validate_player_record(bronze_record)
            bronze_records.append(bronze_record)

    bronze_records = remove_duplicates(bronze_records)

    bronze_records.sort(
        key=lambda record: (
            record["team_name"],
            record["player_name"]
        )
    )

    save_bronze_data(
        bronze_records,
        OUTPUT_FILE
    )

    team_ids = {
        record["team_id"]
        for record in bronze_records
    }

    print(f"Raw player records received: {len(raw_records)}")
    print(f"Records without statistics skipped: {skipped_records}")
    print(f"National teams represented: {len(team_ids)}")
    print(f"Bronze player records created: {len(bronze_records)}")

    if len(team_ids) != 48:
        print(
            "Warning: Expected player records for 48 teams, "
            f"but found {len(team_ids)} teams."
        )
    else:
        print(
            "Validation passed: player data found "
            "for all 48 World Cup teams."
        )

    print(
        "World Cup players Bronze transformation completed."
    )


if __name__ == "__main__":
    main()
