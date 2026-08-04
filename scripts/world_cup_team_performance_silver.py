import json
from collections import defaultdict
from pathlib import Path
from typing import Any


STANDINGS_FILE = Path(
    "data/bronze/world_cup/standings/"
    "world_cup_standings_bronze.json"
)

FIXTURES_FILE = Path(
    "data/bronze/world_cup/fixtures/"
    "world_cup_fixtures_bronze.json"
)

OUTPUT_FOLDER = Path(
    "data/silver/world_cup/team_performance"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_team_performance_silver.json"
)


COMPLETED_STATUSES = {
    "FT",   # Full Time
    "AET",  # After Extra Time
    "PEN"   # After Penalties
}


def load_json(file_path: Path) -> list[dict[str, Any]]:
    """Load and validate a JSON list."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required input file was not found: {file_path}"
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


def safe_percentage(
    numerator: Any,
    denominator: Any
) -> float:
    """Calculate a percentage without division errors."""

    numerator_value = safe_number(numerator)
    denominator_value = safe_number(denominator)

    if denominator_value == 0:
        return 0.0

    return round(
        numerator_value / denominator_value * 100,
        2
    )


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


def normalize_group_name(group_name: Any) -> str | None:
    """Return a cleaner group label."""

    if group_name is None:
        return None

    group_text = str(group_name).strip()

    if "Group" in group_text:
        return group_text

    return f"Group {group_text}"


def determine_fixture_result(
    fixture: dict[str, Any],
    team_id: int
) -> str | None:
    """Return W, D or L for one team in a completed fixture."""

    home_team_id = fixture.get("home_team_id")
    away_team_id = fixture.get("away_team_id")

    home_goals = fixture.get("home_goals")
    away_goals = fixture.get("away_goals")

    if home_goals is None or away_goals is None:
        return None

    home_goals_value = safe_number(home_goals)
    away_goals_value = safe_number(away_goals)

    if team_id == home_team_id:
        team_goals = home_goals_value
        opponent_goals = away_goals_value

    elif team_id == away_team_id:
        team_goals = away_goals_value
        opponent_goals = home_goals_value

    else:
        return None

    if team_goals > opponent_goals:
        return "W"

    if team_goals < opponent_goals:
        return "L"

    return "D"


def build_fixture_metrics(
    fixtures: list[dict[str, Any]]
) -> dict[int, dict[str, Any]]:
    """Aggregate completed fixture metrics for every team."""

    metrics: dict[int, dict[str, Any]] = defaultdict(
        lambda: {
            "completed_fixtures": 0,
            "fixture_wins": 0,
            "fixture_draws": 0,
            "fixture_losses": 0,
            "fixture_goals_for": 0,
            "fixture_goals_against": 0,
            "latest_round": None,
            "rounds_played": []
        }
    )

    for fixture in fixtures:
        status = fixture.get("match_status_short")

        if status not in COMPLETED_STATUSES:
            continue

        home_team_id = fixture.get("home_team_id")
        away_team_id = fixture.get("away_team_id")

        home_goals = safe_number(
            fixture.get("home_goals")
        )
        away_goals = safe_number(
            fixture.get("away_goals")
        )

        round_name = fixture.get("round")

        if home_team_id is not None:
            home_metrics = metrics[home_team_id]

            home_metrics["completed_fixtures"] += 1
            home_metrics["fixture_goals_for"] += home_goals
            home_metrics["fixture_goals_against"] += away_goals

            home_result = determine_fixture_result(
                fixture,
                home_team_id
            )

            if home_result == "W":
                home_metrics["fixture_wins"] += 1
            elif home_result == "D":
                home_metrics["fixture_draws"] += 1
            elif home_result == "L":
                home_metrics["fixture_losses"] += 1

            if round_name:
                home_metrics["latest_round"] = round_name
                home_metrics["rounds_played"].append(round_name)

        if away_team_id is not None:
            away_metrics = metrics[away_team_id]

            away_metrics["completed_fixtures"] += 1
            away_metrics["fixture_goals_for"] += away_goals
            away_metrics["fixture_goals_against"] += home_goals

            away_result = determine_fixture_result(
                fixture,
                away_team_id
            )

            if away_result == "W":
                away_metrics["fixture_wins"] += 1
            elif away_result == "D":
                away_metrics["fixture_draws"] += 1
            elif away_result == "L":
                away_metrics["fixture_losses"] += 1

            if round_name:
                away_metrics["latest_round"] = round_name
                away_metrics["rounds_played"].append(round_name)

    return metrics


def transform_team_performance(
    standing: dict[str, Any],
    fixture_metrics: dict[int, dict[str, Any]]
) -> dict[str, Any]:
    """Create one Silver-layer team performance record."""

    team_id = standing.get("team_id")

    team_fixture_metrics = fixture_metrics.get(
        team_id,
        {
            "completed_fixtures": 0,
            "fixture_wins": 0,
            "fixture_draws": 0,
            "fixture_losses": 0,
            "fixture_goals_for": 0,
            "fixture_goals_against": 0,
            "latest_round": None,
            "rounds_played": []
        }
    )

    matches_played = safe_number(
        standing.get("matches_played")
    )

    wins = safe_number(standing.get("wins"))
    draws = safe_number(standing.get("draws"))
    losses = safe_number(standing.get("losses"))

    goals_for = safe_number(
        standing.get("goals_for")
    )

    goals_against = safe_number(
        standing.get("goals_against")
    )

    points = safe_number(standing.get("points"))

    goals_difference = safe_number(
        standing.get("goals_difference")
    )

    return {
        "team_id": team_id,
        "team_name": standing.get("team_name"),
        "team_logo": standing.get("team_logo"),

        "league_id": standing.get("league_id"),
        "league_name": standing.get("league_name"),
        "season": standing.get("season"),

        "group_name": normalize_group_name(
            standing.get("group_name")
        ),
        "group_rank": standing.get("group_rank"),
        "group_status": standing.get("status"),
        "qualification_description": standing.get(
            "description"
        ),

        "points": int(points),
        "matches_played": int(matches_played),
        "wins": int(wins),
        "draws": int(draws),
        "losses": int(losses),

        "goals_for": int(goals_for),
        "goals_against": int(goals_against),
        "goals_difference": int(goals_difference),

        "win_percentage": safe_percentage(
            wins,
            matches_played
        ),
        "draw_percentage": safe_percentage(
            draws,
            matches_played
        ),
        "loss_percentage": safe_percentage(
            losses,
            matches_played
        ),

        "points_per_match": safe_average(
            points,
            matches_played
        ),
        "goals_for_per_match": safe_average(
            goals_for,
            matches_played
        ),
        "goals_against_per_match": safe_average(
            goals_against,
            matches_played
        ),

        "fixture_matches_played": int(
            team_fixture_metrics["completed_fixtures"]
        ),
        "fixture_wins": int(
            team_fixture_metrics["fixture_wins"]
        ),
        "fixture_draws": int(
            team_fixture_metrics["fixture_draws"]
        ),
        "fixture_losses": int(
            team_fixture_metrics["fixture_losses"]
        ),
        "fixture_goals_for": int(
            team_fixture_metrics["fixture_goals_for"]
        ),
        "fixture_goals_against": int(
            team_fixture_metrics["fixture_goals_against"]
        ),
        "fixture_goal_difference": int(
            team_fixture_metrics["fixture_goals_for"]
            - team_fixture_metrics["fixture_goals_against"]
        ),

        "latest_round": team_fixture_metrics[
            "latest_round"
        ],
        "rounds_played": list(
            dict.fromkeys(
                team_fixture_metrics["rounds_played"]
            )
        ),

        "form": standing.get("form"),
        "updated_at": standing.get("updated_at")
    }


def validate_record(record: dict[str, Any]) -> None:
    """Validate required Silver-layer fields."""

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
            f"Team performance record is missing "
            f"{missing_fields}: {record}"
        )


def save_silver_data(
    records: list[dict[str, Any]]
) -> None:
    """Save the Silver team-performance dataset."""

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
        f"Silver team performance file created: "
        f"{OUTPUT_FILE}"
    )


def main() -> None:
    standings = load_json(STANDINGS_FILE)
    fixtures = load_json(FIXTURES_FILE)

    if not standings:
        raise RuntimeError(
            "The Bronze standings file is empty."
        )

    fixture_metrics = build_fixture_metrics(fixtures)

    silver_records = []

    for standing in standings:
        record = transform_team_performance(
            standing,
            fixture_metrics
        )

        validate_record(record)
        silver_records.append(record)

    silver_records.sort(
        key=lambda record: (
            record["group_name"],
            record["group_rank"],
            record["team_name"]
        )
    )

    save_silver_data(silver_records)

    team_ids = {
        record["team_id"]
        for record in silver_records
    }

    print(f"Standing records loaded: {len(standings)}")
    print(f"Fixture records loaded: {len(fixtures)}")
    print(f"National teams represented: {len(team_ids)}")
    print(f"Silver records created: {len(silver_records)}")

    if len(silver_records) != 48:
        print(
            "Warning: Expected 48 team performance "
            f"records, but created {len(silver_records)}."
        )
    else:
        print(
            "Validation passed: "
            "48 World Cup team records created."
        )

    print(
        "World Cup team performance "
        "Silver transformation completed."
    )


if __name__ == "__main__":
    main()
