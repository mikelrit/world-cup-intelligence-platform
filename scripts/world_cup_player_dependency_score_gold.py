import json
from collections import defaultdict
from pathlib import Path
from typing import Any


INPUT_FILE = Path(
    "data/silver/world_cup/player_performance/"
    "world_cup_player_performance_silver.json"
)

OUTPUT_FOLDER = Path(
    "data/gold/world_cup/player_dependency_score"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_player_dependency_score.json"
)


def load_json(file_path: Path) -> list[dict[str, Any]]:
    """Load and validate the Silver player-performance file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Silver player performance file was not found: {file_path}"
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
    """Convert a value into a float safely."""

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
    """Calculate a percentage safely."""

    numerator_value = safe_number(numerator)
    denominator_value = safe_number(denominator)

    if denominator_value == 0:
        return 0.0

    return round(
        numerator_value / denominator_value * 100,
        2
    )


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


def build_team_totals(
    players: list[dict[str, Any]]
) -> dict[int, dict[str, float]]:
    """Calculate team totals used for dependency shares."""

    totals: dict[int, dict[str, float]] = defaultdict(
        lambda: {
            "minutes": 0.0,
            "goal_contributions": 0.0,
            "defensive_actions": 0.0,
            "key_passes": 0.0
        }
    )

    for player in players:
        team_id = player.get("team_id")

        if team_id is None:
            continue

        totals[team_id]["minutes"] += safe_number(
            player.get("minutes")
        )

        totals[team_id]["goal_contributions"] += safe_number(
            player.get("goal_contributions")
        )

        totals[team_id]["defensive_actions"] += safe_number(
            player.get("defensive_actions")
        )

        totals[team_id]["key_passes"] += safe_number(
            player.get("passes_key")
        )

    return totals


def calculate_global_ranges(
    players: list[dict[str, Any]]
) -> dict[str, tuple[float, float]]:
    """Calculate ranges for globally normalized player metrics."""

    metric_names = [
        "rating",
        "goal_contributions_per_90",
        "duel_success_rate",
        "dribble_success_rate",
        "shots_on_target_rate"
    ]

    ranges: dict[str, tuple[float, float]] = {}

    for metric_name in metric_names:
        values = [
            safe_number(player.get(metric_name))
            for player in players
        ]

        ranges[metric_name] = (
            min(values),
            max(values)
        )

    return ranges


def calculate_dependency_score(
    goal_contribution_share: float,
    minutes_share: float,
    defensive_action_share: float,
    key_pass_share: float,
    rating_score: float,
    per_90_score: float
) -> float:
    """
    Calculate a normalized Player Dependency Score.

    Weights:
    - Team goal-contribution share: 30%
    - Team minutes share: 20%
    - Team defensive-action share: 15%
    - Team key-pass share: 10%
    - Player rating: 15%
    - Goal contributions per 90: 10%
    """

    score = (
        goal_contribution_share * 0.30
        + minutes_share * 0.20
        + defensive_action_share * 0.15
        + key_pass_share * 0.10
        + rating_score * 0.15
        + per_90_score * 0.10
    )

    return round(
        max(0.0, min(100.0, score)),
        2
    )


def transform_player(
    player: dict[str, Any],
    team_totals: dict[int, dict[str, float]],
    global_ranges: dict[str, tuple[float, float]]
) -> dict[str, Any]:
    """Create one Gold Player Dependency record."""

    team_id = player.get("team_id")

    totals = team_totals.get(
        team_id,
        {
            "minutes": 0.0,
            "goal_contributions": 0.0,
            "defensive_actions": 0.0,
            "key_passes": 0.0
        }
    )

    goal_contribution_share = safe_percentage(
        player.get("goal_contributions"),
        totals["goal_contributions"]
    )

    minutes_share = safe_percentage(
        player.get("minutes"),
        totals["minutes"]
    )

    defensive_action_share = safe_percentage(
        player.get("defensive_actions"),
        totals["defensive_actions"]
    )

    key_pass_share = safe_percentage(
        player.get("passes_key"),
        totals["key_passes"]
    )

    rating_min, rating_max = global_ranges["rating"]

    per_90_min, per_90_max = global_ranges[
        "goal_contributions_per_90"
    ]

    duel_min, duel_max = global_ranges[
        "duel_success_rate"
    ]

    dribble_min, dribble_max = global_ranges[
        "dribble_success_rate"
    ]

    shots_min, shots_max = global_ranges[
        "shots_on_target_rate"
    ]

    rating_score = normalize_metric(
        player.get("rating"),
        rating_min,
        rating_max
    )

    per_90_score = normalize_metric(
        player.get("goal_contributions_per_90"),
        per_90_min,
        per_90_max
    )

    duel_score = normalize_metric(
        player.get("duel_success_rate"),
        duel_min,
        duel_max
    )

    dribble_score = normalize_metric(
        player.get("dribble_success_rate"),
        dribble_min,
        dribble_max
    )

    shots_on_target_score = normalize_metric(
        player.get("shots_on_target_rate"),
        shots_min,
        shots_max
    )

    player_dependency_score = calculate_dependency_score(
        goal_contribution_share,
        minutes_share,
        defensive_action_share,
        key_pass_share,
        rating_score,
        per_90_score
    )

    return {
        "player_id": player.get("player_id"),
        "player_name": player.get("player_name"),
        "player_photo": player.get("player_photo"),
        "age": player.get("age"),
        "nationality": player.get("nationality"),
        "position": player.get("position"),

        "team_id": team_id,
        "team_name": player.get("team_name"),
        "team_logo": player.get("team_logo"),

        "league_id": player.get("league_id"),
        "league_name": player.get("league_name"),
        "season": player.get("season"),

        "appearances": int(
            safe_number(player.get("appearances"))
        ),
        "lineups": int(
            safe_number(player.get("lineups"))
        ),
        "minutes": int(
            safe_number(player.get("minutes"))
        ),
        "rating": round(
            safe_number(player.get("rating")),
            2
        ),

        "goals_total": int(
            safe_number(player.get("goals_total"))
        ),
        "goals_assists": int(
            safe_number(player.get("goals_assists"))
        ),
        "goal_contributions": int(
            safe_number(player.get("goal_contributions"))
        ),

        "goals_per_90": safe_number(
            player.get("goals_per_90")
        ),
        "assists_per_90": safe_number(
            player.get("assists_per_90")
        ),
        "goal_contributions_per_90": safe_number(
            player.get("goal_contributions_per_90")
        ),

        "defensive_actions": int(
            safe_number(player.get("defensive_actions"))
        ),
        "passes_key": int(
            safe_number(player.get("passes_key"))
        ),

        "duel_success_rate": safe_number(
            player.get("duel_success_rate")
        ),
        "dribble_success_rate": safe_number(
            player.get("dribble_success_rate")
        ),
        "shots_on_target_rate": safe_number(
            player.get("shots_on_target_rate")
        ),

        "goal_contribution_share": goal_contribution_share,
        "minutes_share": minutes_share,
        "defensive_action_share": defensive_action_share,
        "key_pass_share": key_pass_share,

        "rating_score": rating_score,
        "goal_contributions_per_90_score": per_90_score,
        "duel_score": duel_score,
        "dribble_score": dribble_score,
        "shots_on_target_score": shots_on_target_score,

        "player_dependency_score": player_dependency_score
    }


def validate_record(record: dict[str, Any]) -> None:
    """Validate required Gold player fields."""

    required_fields = [
        "player_id",
        "player_name",
        "team_id",
        "team_name",
        "league_id",
        "season",
        "player_dependency_score"
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Player dependency record is missing "
            f"{missing_fields}: {record}"
        )


def assign_team_ranks(
    records: list[dict[str, Any]]
) -> None:
    """Assign each player a dependency rank within their team."""

    players_by_team: dict[int, list[dict[str, Any]]] = defaultdict(list)

    for record in records:
        players_by_team[record["team_id"]].append(record)

    for team_players in players_by_team.values():
        team_players.sort(
            key=lambda record: (
                -record["player_dependency_score"],
                -record["goal_contributions"],
                record["player_name"]
            )
        )

        for rank, player in enumerate(team_players, start=1):
            player["team_dependency_rank"] = rank


def save_gold_data(
    records: list[dict[str, Any]]
) -> None:
    """Save the Gold Player Dependency dataset."""

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
        f"Gold Player Dependency Score file created: "
        f"{OUTPUT_FILE}"
    )


def main() -> None:
    players = load_json(INPUT_FILE)

    if not players:
        raise RuntimeError(
            "The Silver player performance file is empty."
        )

    team_totals = build_team_totals(players)
    global_ranges = calculate_global_ranges(players)

    gold_records = []

    for player in players:
        record = transform_player(
            player,
            team_totals,
            global_ranges
        )

        validate_record(record)
        gold_records.append(record)

    assign_team_ranks(gold_records)

    gold_records.sort(
        key=lambda record: (
            -record["player_dependency_score"],
            -record["goal_contributions"],
            record["player_name"]
        )
    )

    for global_rank, record in enumerate(
        gold_records,
        start=1
    ):
        record["dependency_rank"] = global_rank

    save_gold_data(gold_records)

    team_ids = {
        record["team_id"]
        for record in gold_records
    }

    print(f"Silver player records loaded: {len(players)}")
    print(f"Gold player records created: {len(gold_records)}")
    print(f"National teams represented: {len(team_ids)}")

    if len(team_ids) != 48:
        print(
            "Warning: Expected 48 national teams, "
            f"but found {len(team_ids)}."
        )
    else:
        print(
            "Validation passed: dependency scores cover "
            "all 48 World Cup teams."
        )

    if gold_records:
        top_player = gold_records[0]

        print(
            "Highest dependency player: "
            f"{top_player['player_name']} "
            f"({top_player['team_name']}) — "
            f"{top_player['player_dependency_score']}"
        )

    print(
        "World Cup Player Dependency Score "
        "Gold transformation completed."
    )


if __name__ == "__main__":
    main()