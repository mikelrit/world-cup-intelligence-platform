import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/bronze/world_cup/fixtures/"
    "world_cup_fixtures_bronze.json"
)

OUTPUT_FOLDER = Path(
    "data/silver/world_cup/match_performance"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_match_performance_silver.json"
)

COMPLETED_STATUSES = {
    "FT",
    "AET",
    "PEN"
}


def load_json(file_path: Path) -> list[dict[str, Any]]:
    """Load and validate the Bronze fixtures file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Bronze fixtures file was not found: {file_path}"
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
    """Convert a value into a number safely."""

    if value is None:
        return 0.0

    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def determine_match_stage(round_name: Any) -> str:
    """Convert the API round description into a broader stage."""

    if round_name is None:
        return "Unknown"

    round_text = str(round_name).lower()

    if "group" in round_text:
        return "Group Stage"

    if "round of 32" in round_text:
        return "Round of 32"

    if "round of 16" in round_text:
        return "Round of 16"

    if "quarter" in round_text:
        return "Quarterfinal"

    if "semi" in round_text:
        return "Semifinal"

    if "third" in round_text:
        return "Third Place"

    if "final" in round_text:
        return "Final"

    return str(round_name)


def determine_result(
    home_goals: Any,
    away_goals: Any,
    status: Any
) -> str | None:
    """Return the result from the home team's perspective."""

    if status not in COMPLETED_STATUSES:
        return None

    if home_goals is None or away_goals is None:
        return None

    home_value = safe_number(home_goals)
    away_value = safe_number(away_goals)

    if home_value > away_value:
        return "Home Win"

    if home_value < away_value:
        return "Away Win"

    return "Draw"


def determine_winner(
    fixture: dict[str, Any]
) -> tuple[Any, Any]:
    """Return the winning team ID and name when available."""

    home_winner = fixture.get("home_team_winner")
    away_winner = fixture.get("away_team_winner")

    if home_winner is True:
        return (
            fixture.get("home_team_id"),
            fixture.get("home_team_name")
        )

    if away_winner is True:
        return (
            fixture.get("away_team_id"),
            fixture.get("away_team_name")
        )

    return None, None


def transform_match(
    fixture: dict[str, Any]
) -> dict[str, Any]:
    """Create one Silver-layer match performance record."""

    home_goals = fixture.get("home_goals")
    away_goals = fixture.get("away_goals")
    status = fixture.get("match_status_short")

    winner_team_id, winner_team_name = determine_winner(
        fixture
    )

    completed = status in COMPLETED_STATUSES

    if completed:
        total_goals = int(
            safe_number(home_goals)
            + safe_number(away_goals)
        )

        goal_difference = int(
            abs(
                safe_number(home_goals)
                - safe_number(away_goals)
            )
        )
    else:
        total_goals = None
        goal_difference = None

    return {
        "fixture_id": fixture.get("fixture_id"),
        "fixture_date": fixture.get("fixture_date"),
        "fixture_timestamp": fixture.get(
            "fixture_timestamp"
        ),

        "league_id": fixture.get("league_id"),
        "league_name": fixture.get("league_name"),
        "season": fixture.get("season"),

        "round": fixture.get("round"),
        "match_stage": determine_match_stage(
            fixture.get("round")
        ),

        "venue_id": fixture.get("venue_id"),
        "venue_name": fixture.get("venue_name"),
        "venue_city": fixture.get("venue_city"),

        "referee": fixture.get("referee"),
        "timezone": fixture.get("timezone"),

        "match_status_long": fixture.get(
            "match_status_long"
        ),
        "match_status_short": status,
        "is_completed": completed,

        "home_team_id": fixture.get("home_team_id"),
        "home_team_name": fixture.get(
            "home_team_name"
        ),
        "home_team_logo": fixture.get(
            "home_team_logo"
        ),

        "away_team_id": fixture.get("away_team_id"),
        "away_team_name": fixture.get(
            "away_team_name"
        ),
        "away_team_logo": fixture.get(
            "away_team_logo"
        ),

        "home_goals": home_goals,
        "away_goals": away_goals,
        "total_goals": total_goals,
        "goal_difference": goal_difference,

        "halftime_home_goals": fixture.get(
            "halftime_home_goals"
        ),
        "halftime_away_goals": fixture.get(
            "halftime_away_goals"
        ),

        "fulltime_home_goals": fixture.get(
            "fulltime_home_goals"
        ),
        "fulltime_away_goals": fixture.get(
            "fulltime_away_goals"
        ),

        "extratime_home_goals": fixture.get(
            "extratime_home_goals"
        ),
        "extratime_away_goals": fixture.get(
            "extratime_away_goals"
        ),

        "penalty_home_goals": fixture.get(
            "penalty_home_goals"
        ),
        "penalty_away_goals": fixture.get(
            "penalty_away_goals"
        ),

        "match_result": determine_result(
            home_goals,
            away_goals,
            status
        ),

        "winner_team_id": winner_team_id,
        "winner_team_name": winner_team_name
    }


def validate_match(record: dict[str, Any]) -> None:
    """Validate required Silver match fields."""

    required_fields = [
        "fixture_id",
        "league_id",
        "season",
        "round",
        "match_stage",
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
            f"Match performance record is missing "
            f"{missing_fields}: {record}"
        )


def remove_duplicates(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Remove duplicate fixtures using fixture_id."""

    unique_matches: dict[int, dict[str, Any]] = {}

    for record in records:
        unique_matches[record["fixture_id"]] = record

    return list(unique_matches.values())


def save_silver_data(
    records: list[dict[str, Any]]
) -> None:
    """Save the Silver match-performance dataset."""

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
        f"Silver match performance file created: "
        f"{OUTPUT_FILE}"
    )


def main() -> None:
    fixtures = load_json(INPUT_FILE)

    if not fixtures:
        raise RuntimeError(
            "The Bronze fixtures file is empty."
        )

    silver_records = []

    for fixture in fixtures:
        record = transform_match(fixture)
        validate_match(record)
        silver_records.append(record)

    silver_records = remove_duplicates(silver_records)

    silver_records.sort(
        key=lambda record: (
            record.get("fixture_timestamp") or 0,
            record["fixture_id"]
        )
    )

    save_silver_data(silver_records)

    completed_matches = sum(
        1
        for record in silver_records
        if record["is_completed"]
    )

    scheduled_matches = (
        len(silver_records) - completed_matches
    )

    stages = {
        record["match_stage"]
        for record in silver_records
    }

    print(f"Bronze fixtures loaded: {len(fixtures)}")
    print(f"Silver match records created: {len(silver_records)}")
    print(f"Completed matches: {completed_matches}")
    print(f"Scheduled or unplayed matches: {scheduled_matches}")
    print(f"Tournament stages represented: {len(stages)}")

    if len(silver_records) != 104:
        print(
            "Warning: Expected 104 World Cup match records, "
            f"but created {len(silver_records)}."
        )
    else:
        print(
            "Validation passed: "
            "104 World Cup match records created."
        )

    print(
        "World Cup match performance "
        "Silver transformation completed."
    )


if __name__ == "__main__":
    main()