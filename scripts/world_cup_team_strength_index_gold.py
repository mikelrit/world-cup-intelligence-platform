import json
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/silver/world_cup/team_performance/"
    "world_cup_team_performance_silver.json"
)

OUTPUT_FOLDER = Path(
    "data/gold/world_cup/team_strength_index"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_team_strength_index.json"
)


def load_json(file_path: Path) -> list[dict[str, Any]]:
    """Load and validate the Silver team-performance file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Silver team performance file was not found: {file_path}"
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


def normalize_metric(
    value: Any,
    minimum: float,
    maximum: float
) -> float:
    """Normalize a metric to a 0–100 scale."""

    numeric_value = safe_number(value)

    if maximum == minimum:
        return 0.0

    normalized = (
        (numeric_value - minimum)
        / (maximum - minimum)
        * 100
    )

    return round(
        max(0.0, min(100.0, normalized)),
        2
    )


def calculate_team_strength_score(
    points_per_match_score: float,
    win_percentage_score: float,
    goal_difference_score: float,
    goals_for_score: float,
    defensive_score: float
) -> float:
    """
    Calculate the Team Strength Index.

    Weights:
    - Points per match: 30%
    - Win percentage: 25%
    - Goal difference per match: 20%
    - Goals scored per match: 15%
    - Defensive performance: 10%
    """

    score = (
        points_per_match_score * 0.30
        + win_percentage_score * 0.25
        + goal_difference_score * 0.20
        + goals_for_score * 0.15
        + defensive_score * 0.10
    )

    return round(score, 2)


def calculate_metric_ranges(
    teams: list[dict[str, Any]]
) -> dict[str, tuple[float, float]]:
    """Calculate minimum and maximum values for normalization."""

    metric_names = [
        "points_per_match",
        "win_percentage",
        "goals_for_per_match",
        "goals_against_per_match"
    ]

    ranges: dict[str, tuple[float, float]] = {}

    for metric_name in metric_names:
        values = [
            safe_number(team.get(metric_name))
            for team in teams
        ]

        ranges[metric_name] = (
            min(values),
            max(values)
        )

    goal_difference_values = []

    for team in teams:
        matches_played = safe_number(
            team.get("matches_played")
        )

        goals_difference = safe_number(
            team.get("goals_difference")
        )

        if matches_played == 0:
            goal_difference_per_match = 0.0
        else:
            goal_difference_per_match = (
                goals_difference / matches_played
            )

        goal_difference_values.append(
            goal_difference_per_match
        )

    ranges["goal_difference_per_match"] = (
        min(goal_difference_values),
        max(goal_difference_values)
    )

    return ranges


def transform_team(
    team: dict[str, Any],
    metric_ranges: dict[str, tuple[float, float]]
) -> dict[str, Any]:
    """Create one Gold team-strength record."""

    matches_played = safe_number(
        team.get("matches_played")
    )

    goals_difference = safe_number(
        team.get("goals_difference")
    )

    if matches_played == 0:
        goal_difference_per_match = 0.0
    else:
        goal_difference_per_match = round(
            goals_difference / matches_played,
            2
        )

    points_min, points_max = metric_ranges[
        "points_per_match"
    ]

    wins_min, wins_max = metric_ranges[
        "win_percentage"
    ]

    goal_diff_min, goal_diff_max = metric_ranges[
        "goal_difference_per_match"
    ]

    goals_for_min, goals_for_max = metric_ranges[
        "goals_for_per_match"
    ]

    goals_against_min, goals_against_max = metric_ranges[
        "goals_against_per_match"
    ]

    points_per_match_score = normalize_metric(
        team.get("points_per_match"),
        points_min,
        points_max
    )

    win_percentage_score = normalize_metric(
        team.get("win_percentage"),
        wins_min,
        wins_max
    )

    goal_difference_score = normalize_metric(
        goal_difference_per_match,
        goal_diff_min,
        goal_diff_max
    )

    goals_for_score = normalize_metric(
        team.get("goals_for_per_match"),
        goals_for_min,
        goals_for_max
    )

    # Lower goals conceded is better, so reverse the scale.
    defensive_score = (
        100
        - normalize_metric(
            team.get("goals_against_per_match"),
            goals_against_min,
            goals_against_max
        )
    )

    team_strength_score = calculate_team_strength_score(
        points_per_match_score,
        win_percentage_score,
        goal_difference_score,
        goals_for_score,
        defensive_score
    )

    return {
        "team_id": team.get("team_id"),
        "team_name": team.get("team_name"),
        "team_logo": team.get("team_logo"),

        "league_id": team.get("league_id"),
        "league_name": team.get("league_name"),
        "season": team.get("season"),

        "group_name": team.get("group_name"),
        "group_rank": team.get("group_rank"),
        "group_status": team.get("group_status"),
        "qualification_description": team.get(
            "qualification_description"
        ),

        "points": int(
            safe_number(team.get("points"))
        ),
        "matches_played": int(matches_played),
        "wins": int(
            safe_number(team.get("wins"))
        ),
        "draws": int(
            safe_number(team.get("draws"))
        ),
        "losses": int(
            safe_number(team.get("losses"))
        ),

        "goals_for": int(
            safe_number(team.get("goals_for"))
        ),
        "goals_against": int(
            safe_number(team.get("goals_against"))
        ),
        "goals_difference": int(goals_difference),

        "points_per_match": safe_number(
            team.get("points_per_match")
        ),
        "win_percentage": safe_number(
            team.get("win_percentage")
        ),
        "goals_for_per_match": safe_number(
            team.get("goals_for_per_match")
        ),
        "goals_against_per_match": safe_number(
            team.get("goals_against_per_match")
        ),
        "goal_difference_per_match": (
            goal_difference_per_match
        ),

        "points_per_match_score": (
            points_per_match_score
        ),
        "win_percentage_score": (
            win_percentage_score
        ),
        "goal_difference_score": (
            goal_difference_score
        ),
        "goals_for_score": goals_for_score,
        "defensive_score": round(
            defensive_score,
            2
        ),

        "team_strength_score": (
            team_strength_score
        )
    }


def validate_record(record: dict[str, Any]) -> None:
    """Validate required Gold-layer fields."""

    required_fields = [
        "team_id",
        "team_name",
        "league_id",
        "season",
        "group_name",
        "team_strength_score"
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Team strength record is missing "
            f"{missing_fields}: {record}"
        )


def save_gold_data(
    records: list[dict[str, Any]]
) -> None:
    """Save the Gold Team Strength Index dataset."""

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
        f"Gold Team Strength Index file created: "
        f"{OUTPUT_FILE}"
    )


def main() -> None:
    teams = load_json(INPUT_FILE)

    if not teams:
        raise RuntimeError(
            "The Silver team performance file is empty."
        )

    metric_ranges = calculate_metric_ranges(teams)

    gold_records = []

    for team in teams:
        record = transform_team(
            team,
            metric_ranges
        )

        validate_record(record)
        gold_records.append(record)

    gold_records.sort(
        key=lambda record: (
            -record["team_strength_score"],
            record["team_name"]
        )
    )

    for index, record in enumerate(
        gold_records,
        start=1
    ):
        record["strength_rank"] = index

    save_gold_data(gold_records)

    print(f"Silver team records loaded: {len(teams)}")
    print(f"Gold team records created: {len(gold_records)}")

    if len(gold_records) != 48:
        print(
            "Warning: Expected 48 Team Strength records, "
            f"but created {len(gold_records)}."
        )
    else:
        print(
            "Validation passed: "
            "48 Team Strength records created."
        )

    if gold_records:
        print(
            "Highest-ranked team: "
            f"{gold_records[0]['team_name']} "
            f"({gold_records[0]['team_strength_score']})"
        )

    print(
        "World Cup Team Strength Index "
        "Gold transformation completed."
    )


if __name__ == "__main__":
    main()
