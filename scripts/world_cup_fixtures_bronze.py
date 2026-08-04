import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/raw/world_cup/fixtures/world_cup_fixtures_raw.json"
)

OUTPUT_FOLDER = Path(
    "data/bronze/world_cup/fixtures"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_fixtures_bronze.json"
)


def load_raw_data(file_path: Path) -> dict[str, Any]:
    """Load the untouched World Cup fixtures API response."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw fixtures file was not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    api_errors = data.get("errors", {})

    if api_errors:
        raise RuntimeError(
            f"Raw API file contains errors: {api_errors}"
        )

    return data


def transform_fixture(
    record: dict[str, Any]
) -> dict[str, Any]:
    """Flatten one World Cup fixture into a Bronze-layer record."""

    fixture = record.get("fixture") or {}
    league = record.get("league") or {}
    teams = record.get("teams") or {}
    goals = record.get("goals") or {}
    score = record.get("score") or {}

    venue = fixture.get("venue") or {}
    status = fixture.get("status") or {}

    home_team = teams.get("home") or {}
    away_team = teams.get("away") or {}

    halftime = score.get("halftime") or {}
    fulltime = score.get("fulltime") or {}
    extratime = score.get("extratime") or {}
    penalty = score.get("penalty") or {}

    return {
        "fixture_id": fixture.get("id"),
        "referee": fixture.get("referee"),
        "timezone": fixture.get("timezone"),
        "fixture_date": fixture.get("date"),
        "fixture_timestamp": fixture.get("timestamp"),

        "venue_id": venue.get("id"),
        "venue_name": venue.get("name"),
        "venue_city": venue.get("city"),

        "match_status_long": status.get("long"),
        "match_status_short": status.get("short"),
        "elapsed_minutes": status.get("elapsed"),
        "extra_minutes": status.get("extra"),

        "league_id": league.get("id"),
        "league_name": league.get("name"),
        "league_country": league.get("country"),
        "league_logo": league.get("logo"),
        "league_flag": league.get("flag"),
        "season": league.get("season"),
        "round": league.get("round"),

        "home_team_id": home_team.get("id"),
        "home_team_name": home_team.get("name"),
        "home_team_logo": home_team.get("logo"),
        "home_team_winner": home_team.get("winner"),

        "away_team_id": away_team.get("id"),
        "away_team_name": away_team.get("name"),
        "away_team_logo": away_team.get("logo"),
        "away_team_winner": away_team.get("winner"),

        "home_goals": goals.get("home"),
        "away_goals": goals.get("away"),

        "halftime_home_goals": halftime.get("home"),
        "halftime_away_goals": halftime.get("away"),

        "fulltime_home_goals": fulltime.get("home"),
        "fulltime_away_goals": fulltime.get("away"),

        "extratime_home_goals": extratime.get("home"),
        "extratime_away_goals": extratime.get("away"),

        "penalty_home_goals": penalty.get("home"),
        "penalty_away_goals": penalty.get("away")
    }


def validate_fixture(
    record: dict[str, Any]
) -> None:
    """Validate the fields required for each fixture."""

    required_fields = [
        "fixture_id",
        "league_id",
        "season",
        "round",
        "home_team_id",
        "home_team_name",
        "away_team_id",
        "away_team_name"
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Fixture record is missing required fields "
            f"{missing_fields}: {record}"
        )


def remove_duplicates(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Remove duplicate fixtures using fixture_id."""

    unique_fixtures: dict[int, dict[str, Any]] = {}

    for record in records:
        fixture_id = record["fixture_id"]
        unique_fixtures[fixture_id] = record

    return list(unique_fixtures.values())


def save_bronze_data(
    records: list[dict[str, Any]],
    output_file: Path
) -> None:
    """Save flattened fixtures to the Bronze layer."""

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

    print(f"Bronze fixtures file created: {output_file}")


def main() -> None:
    raw_data = load_raw_data(INPUT_FILE)

    raw_records = raw_data.get("response", [])

    if not raw_records:
        raise RuntimeError(
            "No World Cup fixture records were found "
            "in the Raw file."
        )

    bronze_records = []

    for raw_record in raw_records:
        bronze_record = transform_fixture(raw_record)
        validate_fixture(bronze_record)
        bronze_records.append(bronze_record)

    bronze_records = remove_duplicates(bronze_records)

    bronze_records.sort(
        key=lambda record: (
            record.get("fixture_timestamp") or 0,
            record["fixture_id"]
        )
    )

    save_bronze_data(
        bronze_records,
        OUTPUT_FILE
    )

    print(f"Raw records received: {len(raw_records)}")
    print(f"Bronze records created: {len(bronze_records)}")

    if len(bronze_records) != 104:
        print(
            "Warning: Expected 104 World Cup fixtures, "
            f"but created {len(bronze_records)}."
        )
    else:
        print(
            "Validation passed: "
            "104 World Cup fixtures created."
        )

    print(
        "World Cup fixtures Bronze transformation completed."
    )


if __name__ == "__main__":
    main()