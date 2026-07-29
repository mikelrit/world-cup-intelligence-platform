import json
from pathlib import Path


TEAM_FILE = Path("data/gold/team_strength_index/team_strength_index.json")
PLAYER_FILE = Path("data/gold/player_dependency_score/player_dependency_score.json")


with open(TEAM_FILE, "r") as file:
    teams = json.load(file)

with open(PLAYER_FILE, "r") as file:
    players = json.load(file)

team_ids = {team.get("team_id") for team in teams}
player_team_ids = {player.get("team_id") for player in players}

print("Team Strength IDs:")
print(sorted(team_ids))

print("\nPlayer Dependency Team IDs:")
print(sorted(player_team_ids))

print("\nMatching IDs:")
print(sorted(team_ids.intersection(player_team_ids)))

print("\nTeams with no matching players:")
print(sorted(team_ids - player_team_ids))