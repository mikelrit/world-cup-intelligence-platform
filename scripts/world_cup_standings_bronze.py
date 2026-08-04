import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/raw/world_cup/standings/world_cup_standings_raw.json"
)

OUTPUT_FOLDER = Path(
    "data/bronze/world_cup/standings"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_standings_bronze.json"
)


def load_raw_data(file_path: Path) -> dict[str, Any]:
    """Load the untouched World Cup standings response."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw standings file was not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    api_errors = data.get("errors", {})

    if api_errors:
        raise RuntimeError(
            f"Raw API file contains errors: {api_errors}"
        )

    return data


def transform_standing(
    standing: dict[str, Any],
    league: dict[str, Any]
) -> dict[str, Any]:
    """Flatten one World Cup standing row."""

    team = standing.get("team") or {}
    all_stats = standing.get("all") or {}
    goals = all_stats.get("goals") or {}

    return {
        "league_id": league.get("id"),
        "league_name": league.get("name"),
        "league_country": league.get("country"),
        "season": league.get("season"),

        "group_name": standing.get("group"),
        "group_rank": standing.get("rank"),

        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "team_logo": team.get("logo"),

        "points": standing.get("points"),
        "goals_difference": standing.get("goalsDiff"),
        "form": standing.get("form"),
        "status": standing.get("status"),
        "description": standing.get("description"),

        "matches_played": all_stats.get("played"),
        "wins": all_stats.get("win"),
        "draws": all_stats.get("draw"),
        "losses": all_stats.get("lose"),

        "goals_for": goals.get("for"),
        "goals_against": goals.get("against"),

        "updated_at": standing.get("update")
    }


def validate_standing(record: dict[str, Any]) -> None:
    """Validate required Bronze standing fields."""

    required_fields = [
        "league_id",
        "season",
        "group_name",
        "group_rank",
        "team_id",
        "team_name"
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Standing record is missing required fields "
            f"{missing_fields}: {record}"
        )


def remove_duplicates(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Remove duplicate team standings within a group."""

    unique_records: dict[
        tuple[Any, Any, Any],
        dict[str, Any]
    ] = {}

    for record in records:
        key = (
            record["league_id"],
            record["season"],
            record["team_id"]
        )

        unique_records[key] = record

    return list(unique_records.values())


def save_bronze_data(
    records: list[dict[str, Any]],
    output_file: Path
) -> None:
    """Save flattened standings records."""

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

    print(f"Bronze standings file created: {output_file}")


def main() -> None:
    raw_data = load_raw_data(INPUT_FILE)

    responses = raw_data.get("response", [])

    if not responses:
        raise RuntimeError(
            "No World Cup standings response was found."
        )

    bronze_records = []

    for response_record in responses:
        league = response_record.get("league") or {}
        groups = league.get("standings") or []

        for group in groups:
            for standing in group:
                bronze_record = transform_standing(
                    standing,
                    league
                )

                validate_standing(bronze_record)
                bronze_records.append(bronze_record)

    bronze_records = remove_duplicates(bronze_records)

    bronze_records.sort(
        key=lambda record: (
            record["group_name"],
            record["group_rank"],
            record["team_name"]
        )
    )

    save_bronze_data(
        bronze_records,
        OUTPUT_FILE
    )

    group_names = {
        record["group_name"]
        for record in bronze_records
    }

    print(f"Groups transformed: {len(group_names)}")
    print(f"Bronze records created: {len(bronze_records)}")

    if len(group_names) != 12:
        print(
            "Warning: Expected 12 groups, "
            f"but created {len(group_names)}."
        )
    else:
        print("Validation passed: 12 groups created.")

    if len(bronze_records) != 48:
        print(
            "Warning: Expected 48 standing rows, "
            f"but created {len(bronze_records)}."
        )
    else:
        print(
            "Validation passed: "
            "48 World Cup standing rows created."
        )

    print(
        "World Cup standings Bronze transformation completed."
    )


if __name__ == "__main__":
    main()