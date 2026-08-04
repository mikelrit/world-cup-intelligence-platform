# World Cup Intelligence Platform

An end-to-end football analytics platform built with Python and Power
BI that transforms raw API-Football data into interactive dashboards
and analytical insights for the 2026 FIFA World Cup.

---

## Overview

The World Cup Intelligence Platform follows a modern
Bronze–Silver–Gold data architecture to collect, transform, model, and
visualize tournament data.

The project combines automated Python data pipelines with interactive
Power BI dashboards to analyze teams, players, and tournament
performance.

---

## Features

- Executive tournament overview
- World Cup power rankings
- Team analysis dashboard
- Player analysis dashboard
- Tournament leaders dashboard
- Team Strength Index
- Player Dependency Score
- World Cup Power Score
- Interactive Power BI visualizations

---

## Dashboard Pages

### Executive Overview

High-level tournament summary including:

- Teams analyzed
- Average Team Strength
- Average Power Score
- Highest ranked nation
- Top player

---

### Tournament Leaders

Highlights the tournament leaders for:

- Goals
- Assists
- Goal Contributions
- Player Dependency Score

---

### World Cup Power Rankings

Ranks all national teams using the custom World Cup Power Score while comparing:

- Team Strength
- Average Player Dependency
- Key Player
- Team Rankings

---

### Team Analysis

Analyze an individual national team including:

- Team Strength
- Power Score
- Average Player Dependency
- Key Player
- Player influence
- Team comparison metrics

---

### Player Analysis

Analyze players within each national team including:

- Goal Contributions
- Dependency Score
- Most Influential Player
- Team player rankings

---

## Data Pipeline

```
API-Football
      │
      ▼
 Ingestion Scripts
      │
      ▼
 Bronze Layer
      │
      ▼
 Silver Layer
      │
      ▼
 Gold Layer
      │
      ▼
 Power BI Dashboard
```

---

## Repository Structure

```
world-cup-intelligence-platform/

├── api-tests/
├── dashboards/
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docs/
│   └── dashboard_screenshots/
├── scripts/
├── planning/
├── research/
├── .gitignore
└── README.md
```

---

## Technology Stack

- Python
- Pandas
- Power BI
- Power Query
- DAX
- API-Football
- JSON
- Git
- GitHub

---

## Analytical Models

### Team Strength Index

A custom metric designed to evaluate the overall strength of each
national team using tournament performance statistics.

### Player Dependency Score

Measures how heavily a national team relies on an individual player
based on their statistical contributions.

### World Cup Power Score

A composite metric combining team performance and player influence to
generate tournament power rankings.

---

## Dashboard

The interactive Power BI dashboard is included in the **dashboards/** folder.

Screenshots of each report page are available in:

```
docs/dashboard_screenshots/
```

---

## Project Status

**Completed**

- Data pipeline complete
- Bronze, Silver, and Gold layers complete
- Power BI dashboard complete
- Interactive reports complete
- Repository finalized

---

## Author

**Mikel Nwankwor**

Rochester Institute of Technology

Computing & Information Technologies

Cybersecurity Minor
