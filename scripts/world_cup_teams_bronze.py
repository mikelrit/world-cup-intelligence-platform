import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/raw/world_cup/teams/world_cup_teams_raw.json"
)

OUTPUT_FOLDER = Path(
    "data/bronze/world_cup/teams"
)

OUTPUT_FILE = OUTPUT_FOLDER / "world_cup_teams_bronze.json"


def load_raw_data(file_path: Path) -> dict[str, Any]:
    """Load the untouched World Cup teams API response."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw teams file was not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    api_errors = data.get("errors", {})

    if api_errors:
        raise RuntimeError(
            f"Raw API file contains errors: {api_errors}"
        )

    return data


def transform_team(record: dict[str, Any]) -> dict[str, Any]:
    """Flatten one API team record into a Bronze-layer record."""

    team = record.get("team") or {}
    venue = record.get("venue") or {}

    return {
        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "team_code": team.get("code"),
        "country": team.get("country"),
        "founded": team.get("founded"),
        "national_team": team.get("national"),
        "team_logo": team.get("logo"),
        "venue_id": venue.get("id"),
        "venue_name": venue.get("name"),
        "venue_address": venue.get("address"),
        "venue_city": venue.get("city"),
        "venue_capacity": venue.get("capacity"),
        "venue_surface": venue.get("surface"),
        "venue_image": venue.get("image"),
        "league_id": 1,
        "league_name": "FIFA World Cup",
        "season": 2026,
    }


def validate_team(record: dict[str, Any]) -> None:
    """Validate required Bronze-layer team fields."""

    required_fields = [
        "team_id",
        "team_name",
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Team record is missing required fields "
            f"{missing_fields}: {record}"
        )


def remove_duplicates(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Remove duplicate teams using team_id as the unique key."""

    unique_teams: dict[int, dict[str, Any]] = {}

    for record in records:
        team_id = record["team_id"]
        unique_teams[team_id] = record

    return list(unique_teams.values())


def save_bronze_data(
    records: list[dict[str, Any]],
    output_file: Path
) -> None:
    """Save clean Bronze-layer team records."""

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Bronze teams file created: {output_file}")


def main() -> None:
    raw_data = load_raw_data(INPUT_FILE)

    raw_records = raw_data.get("response", [])

    if not raw_records:
        raise RuntimeError(
            "No World Cup team records were found in the Raw file."
        )

    bronze_records = []

    for raw_record in raw_records:
        bronze_record = transform_team(raw_record)
        validate_team(bronze_record)
        bronze_records.append(bronze_record)

    bronze_records = remove_duplicates(bronze_records)

    bronze_records.sort(
        key=lambda record: record["team_name"]
    )

    save_bronze_data(
        bronze_records,
        OUTPUT_FILE
    )

    print(f"Raw records received: {len(raw_records)}")
    print(f"Bronze records created: {len(bronze_records)}")

    if len(bronze_records) != 48:
        print(
            "Warning: Expected 48 World Cup teams, "
            f"but created {len(bronze_records)}."
        )
    else:
        print("Validation passed: 48 World Cup teams created.")

    print("World Cup teams Bronze transformation completed.")


if __name__ == "__main__":
    main()