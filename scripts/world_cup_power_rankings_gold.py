import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


TEAM_STRENGTH_FILE = Path(
    "data/gold/world_cup/team_strength_index/"
    "world_cup_team_strength_index.json"
)

PLAYER_DEPENDENCY_FILE = Path(
    "data/gold/world_cup/player_dependency_score/"
    "world_cup_player_dependency_score.json"
)

OUTPUT_FOLDER = Path(
    "data/gold/world_cup/world_cup_power_rankings"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER / "world_cup_power_rankings.json"
)


def load_json(file_path: Path) -> list[dict[str, Any]]:
    """Load and validate a JSON list."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required Gold input file was not found: {file_path}"
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


def calculate_average(values: list[float]) -> float:
    """Calculate an average safely."""

    if not values:
        return 0.0

    return round(mean(values), 2)


def group_players_by_team(
    players: list[dict[str, Any]]
) -> dict[tuple[Any, Any, Any], list[dict[str, Any]]]:
    """Group player dependency records by team, league and season."""

    grouped_players: dict[
        tuple[Any, Any, Any],
        list[dict[str, Any]]
    ] = defaultdict(list)

    for player in players:
        key = (
            player.get("team_id"),
            player.get("league_id"),
            player.get("season")
        )

        grouped_players[key].append(player)

    return grouped_players


def select_top_player(
    players: list[dict[str, Any]]
) -> dict[str, Any] | None:
    """Return the highest-dependency player for one team."""

    if not players:
        return None

    return max(
        players,
        key=lambda player: (
            safe_number(
                player.get("player_dependency_score")
            ),
            safe_number(
                player.get("goal_contributions")
            ),
            safe_number(
                player.get("minutes")
            )
        )
    )


def calculate_power_score(
    team_strength_score: float,
    average_player_dependency_score: float,
    top_player_dependency_score: float
) -> float:
    """
    Calculate the final World Cup Power Score.

    Weights:
    - Team Strength Index: 70%
    - Average Player Dependency: 20%
    - Top Player Dependency: 10%

    All component scores are already normalized to 0–100,
    so the final score also remains between 0 and 100.
    """

    score = (
        team_strength_score * 0.70
        + average_player_dependency_score * 0.20
        + top_player_dependency_score * 0.10
    )

    return round(
        max(0.0, min(100.0, score)),
        2
    )


def transform_team(
    team: dict[str, Any],
    players_by_team: dict[
        tuple[Any, Any, Any],
        list[dict[str, Any]]
    ]
) -> dict[str, Any]:
    """Create one final World Cup Power Ranking record."""

    team_key = (
        team.get("team_id"),
        team.get("league_id"),
        team.get("season")
    )

    team_players = players_by_team.get(
        team_key,
        []
    )

    dependency_scores = [
        safe_number(
            player.get("player_dependency_score")
        )
        for player in team_players
    ]

    average_player_dependency_score = (
        calculate_average(dependency_scores)
    )

    top_player = select_top_player(team_players)

    if top_player is None:
        top_player_id = None
        top_player_name = None
        top_player_position = None
        top_player_photo = None
        top_player_dependency_score = 0.0
        top_player_goal_contributions = 0
    else:
        top_player_id = top_player.get("player_id")
        top_player_name = top_player.get("player_name")
        top_player_position = top_player.get("position")
        top_player_photo = top_player.get("player_photo")

        top_player_dependency_score = safe_number(
            top_player.get("player_dependency_score")
        )

        top_player_goal_contributions = int(
            safe_number(
                top_player.get("goal_contributions")
            )
        )

    total_goal_contributions = int(
        sum(
            safe_number(
                player.get("goal_contributions")
            )
            for player in team_players
        )
    )

    total_player_minutes = int(
        sum(
            safe_number(
                player.get("minutes")
            )
            for player in team_players
        )
    )

    players_analyzed = len(team_players)

    team_strength_score = safe_number(
        team.get("team_strength_score")
    )

    world_cup_power_score = calculate_power_score(
        team_strength_score,
        average_player_dependency_score,
        top_player_dependency_score
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

        "matches_played": int(
            safe_number(team.get("matches_played"))
        ),
        "wins": int(
            safe_number(team.get("wins"))
        ),
        "draws": int(
            safe_number(team.get("draws"))
        ),
        "losses": int(
            safe_number(team.get("losses"))
        ),

        "points": int(
            safe_number(team.get("points"))
        ),
        "goals_for": int(
            safe_number(team.get("goals_for"))
        ),
        "goals_against": int(
            safe_number(team.get("goals_against"))
        ),
        "goals_difference": int(
            safe_number(team.get("goals_difference"))
        ),

        "strength_rank": team.get("strength_rank"),
        "team_strength_score": round(
            team_strength_score,
            2
        ),

        "players_analyzed": players_analyzed,
        "total_player_minutes": total_player_minutes,
        "total_goal_contributions": total_goal_contributions,

        "average_player_dependency_score": (
            average_player_dependency_score
        ),

        "top_player_id": top_player_id,
        "top_player_name": top_player_name,
        "top_player_position": top_player_position,
        "top_player_photo": top_player_photo,
        "top_player_dependency_score": round(
            top_player_dependency_score,
            2
        ),
        "top_player_goal_contributions": (
            top_player_goal_contributions
        ),

        "world_cup_power_score": world_cup_power_score
    }


def validate_record(record: dict[str, Any]) -> None:
    """Validate required final Gold fields."""

    required_fields = [
        "team_id",
        "team_name",
        "league_id",
        "season",
        "group_name",
        "team_strength_score",
        "world_cup_power_score"
    ]

    missing_fields = [
        field
        for field in required_fields
        if record.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Power ranking record is missing "
            f"{missing_fields}: {record}"
        )


def save_gold_data(
    records: list[dict[str, Any]]
) -> None:
    """Save the final World Cup Power Rankings dataset."""

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
        f"Gold World Cup Power Rankings file created: "
        f"{OUTPUT_FILE}"
    )


def main() -> None:
    teams = load_json(TEAM_STRENGTH_FILE)
    players = load_json(PLAYER_DEPENDENCY_FILE)

    if not teams:
        raise RuntimeError(
            "The Team Strength Index file is empty."
        )

    if not players:
        raise RuntimeError(
            "The Player Dependency Score file is empty."
        )

    players_by_team = group_players_by_team(players)

    gold_records = []

    teams_without_players = []

    for team in teams:
        record = transform_team(
            team,
            players_by_team
        )

        validate_record(record)
        gold_records.append(record)

        if record["players_analyzed"] == 0:
            teams_without_players.append(
                record["team_name"]
            )

    gold_records.sort(
        key=lambda record: (
            -record["world_cup_power_score"],
            -record["team_strength_score"],
            record["team_name"]
        )
    )

    for rank, record in enumerate(
        gold_records,
        start=1
    ):
        record["world_cup_rank"] = rank

    save_gold_data(gold_records)

    print(f"Team Strength records loaded: {len(teams)}")
    print(f"Player Dependency records loaded: {len(players)}")
    print(f"Final ranking records created: {len(gold_records)}")

    if len(gold_records) != 48:
        print(
            "Warning: Expected 48 World Cup ranking records, "
            f"but created {len(gold_records)}."
        )
    else:
        print(
            "Validation passed: "
            "48 World Cup ranking records created."
        )

    if teams_without_players:
        print(
            "Warning: No player records matched these teams:"
        )

        for team_name in teams_without_players:
            print(f"- {team_name}")
    else:
        print(
            "Validation passed: player data matched "
            "all 48 national teams."
        )

    if gold_records:
        top_team = gold_records[0]

        print(
            "Highest-ranked team: "
            f"{top_team['team_name']} — "
            f"{top_team['world_cup_power_score']}"
        )

    unique_power_scores = {
        record["world_cup_power_score"]
        for record in gold_records
    }

    if len(unique_power_scores) == 1:
        print(
            "Note: Every team currently has the same power score. "
            "This can occur when tournament performance statistics "
            "have not yet been recorded."
        )

    print(
        "World Cup Power Rankings "
        "Gold transformation completed."
    )


if __name__ == "__main__":
    main()
