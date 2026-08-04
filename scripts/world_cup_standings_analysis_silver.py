import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/bronze/world_cup/standings/"
    "world_cup_standings_bronze.json"
)

OUTPUT_FOLDER = Path(
    "data/silver/world_cup/standings_analysis"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_standings_analysis_silver.json"
)


def load_json(file_path: Path) -> list[dict[str, Any]]:
    """Load and validate the Bronze standings file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Bronze standings file was not found: {file_path}"
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


def safe_average(
    numerator: Any,
    denominator: Any
) -> float:
    """Calculate a decimal average safely."""

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


def normalize_group_name(group_name: Any) -> str | None:
    """Standardize the World Cup group name."""

    if group_name is None:
        return None

    group_text = str(group_name).strip()

    if group_text.lower().startswith("group"):
        return group_text

    return f"Group {group_text}"


def determine_qualification_status(
    rank: int,
    description: Any,
    status: Any
) -> str:
    """
    Estimate group-stage qualification status.

    The 2026 World Cup format advances:
    - the top two teams in each group
    - the eight best third-place teams

    Third-place teams are therefore marked as provisional.
    """

    description_text = str(description or "").lower()
    status_text = str(status or "").lower()

    if "qualified" in description_text:
        return "Qualified"

    if "eliminated" in description_text:
        return "Eliminated"

    if status_text in {"same", "up"} and rank <= 2:
        return "Qualification Position"

    if rank <= 2:
        return "Qualification Position"

    if rank == 3:
        return "Third-Place Contender"

    return "Elimination Position"


def calculate_group_performance_score(
    points_per_match: float,
    win_percentage: float,
    goals_difference: float,
    goals_for_per_match: float,
    goals_against_per_match: float
) -> float:
    """
    Calculate a preliminary group-performance score.

    This is a Silver-layer analytical metric, not the final
    Gold-layer Team Strength Index.
    """

    defensive_component = max(
        0.0,
        3.0 - goals_against_per_match
    )

    score = (
        points_per_match * 25
        + win_percentage * 0.35
        + goals_difference * 5
        + goals_for_per_match * 10
        + defensive_component * 5
    )

    return round(score, 2)


def transform_standing(
    standing: dict[str, Any]
) -> dict[str, Any]:
    """Create one Silver standings-analysis record."""

    matches_played = int(
        safe_number(
            standing.get("matches_played")
        )
    )

    wins = int(
        safe_number(
            standing.get("wins")
        )
    )

    draws = int(
        safe_number(
            standing.get("draws")
        )
    )

    losses = int(
        safe_number(
            standing.get("losses")
        )
    )

    points = int(
        safe_number(
            standing.get("points")
        )
    )

    goals_for = int(
        safe_number(
            standing.get("goals_for")
        )
    )

    goals_against = int(
        safe_number(
            standing.get("goals_against")
        )
    )

    goals_difference = int(
        safe_number(
            standing.get("goals_difference")
        )
    )

    group_rank = int(
        safe_number(
            standing.get("group_rank")
        )
    )

    points_per_match = safe_average(
        points,
        matches_played
    )

    goals_for_per_match = safe_average(
        goals_for,
        matches_played
    )

    goals_against_per_match = safe_average(
        goals_against,
        matches_played
    )

    win_percentage = safe_percentage(
        wins,
        matches_played
    )

    draw_percentage = safe_percentage(
        draws,
        matches_played
    )

    loss_percentage = safe_percentage(
        losses,
        matches_played
    )

    goal_difference_per_match = safe_average(
        goals_difference,
        matches_played
    )

    qualification_status = determine_qualification_status(
        group_rank,
        standing.get("description"),
        standing.get("status")
    )

    group_performance_score = (
        calculate_group_performance_score(
            points_per_match,
            win_percentage,
            goals_difference,
            goals_for_per_match,
            goals_against_per_match
        )
    )

    return {
        "team_id": standing.get("team_id"),
        "team_name": standing.get("team_name"),
        "team_logo": standing.get("team_logo"),

        "league_id": standing.get("league_id"),
        "league_name": standing.get("league_name"),
        "season": standing.get("season"),

        "group_name": normalize_group_name(
            standing.get("group_name")
        ),
        "group_rank": group_rank,

        "points": points,
        "matches_played": matches_played,
        "wins": wins,
        "draws": draws,
        "losses": losses,

        "goals_for": goals_for,
        "goals_against": goals_against,
        "goals_difference": goals_difference,

        "points_per_match": points_per_match,
        "goals_for_per_match": goals_for_per_match,
        "goals_against_per_match": goals_against_per_match,
        "goal_difference_per_match": goal_difference_per_match,

        "win_percentage": win_percentage,
        "draw_percentage": draw_percentage,
        "loss_percentage": loss_percentage,

        "form": standing.get("form"),
        "standing_status": standing.get("status"),
        "qualification_description": standing.get(
            "description"
        ),
        "qualification_status": qualification_status,

        "group_performance_score": group_performance_score,
        "updated_at": standing.get("updated_at")
    }


def validate_record(record: dict[str, Any]) -> None:
    """Validate required Silver standings fields."""

    required_fields = [
        "team_id",
        "team_name",
        "league_id",
        "season",
        "group_name",
        "group_rank"
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Standings analysis record is missing "
            f"{missing_fields}: {record}"
        )


def remove_duplicates(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Remove duplicate team standings records."""

    unique_records: dict[
        tuple[Any, Any, Any],
        dict[str, Any]
    ] = {}

    for record in records:
        key = (
            record["team_id"],
            record["league_id"],
            record["season"]
        )

        unique_records[key] = record

    return list(unique_records.values())


def save_silver_data(
    records: list[dict[str, Any]]
) -> None:
    """Save the Silver standings-analysis dataset."""

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
        f"Silver standings analysis file created: "
        f"{OUTPUT_FILE}"
    )


def main() -> None:
    standings = load_json(INPUT_FILE)

    if not standings:
        raise RuntimeError(
            "The Bronze standings file is empty."
        )

    silver_records = []

    for standing in standings:
        record = transform_standing(standing)
        validate_record(record)
        silver_records.append(record)

    silver_records = remove_duplicates(silver_records)

    silver_records.sort(
        key=lambda record: (
            record["group_name"],
            record["group_rank"],
            record["team_name"]
        )
    )

    save_silver_data(silver_records)

    group_names = {
        record["group_name"]
        for record in silver_records
    }

    qualification_positions = sum(
        1
        for record in silver_records
        if record["qualification_status"]
        == "Qualification Position"
    )

    third_place_contenders = sum(
        1
        for record in silver_records
        if record["qualification_status"]
        == "Third-Place Contender"
    )

    print(f"Bronze standings loaded: {len(standings)}")
    print(f"Groups represented: {len(group_names)}")
    print(f"Silver records created: {len(silver_records)}")
    print(
        f"Top-two qualification positions: "
        f"{qualification_positions}"
    )
    print(
        f"Third-place contenders: "
        f"{third_place_contenders}"
    )

    if len(silver_records) != 48:
        print(
            "Warning: Expected 48 standings analysis "
            f"records, but created {len(silver_records)}."
        )
    else:
        print(
            "Validation passed: "
            "48 World Cup standings records created."
        )

    print(
        "World Cup standings analysis "
        "Silver transformation completed."
    )


if __name__ == "__main__":
    main()
