# 🌍 World Cup Intelligence Platform (WCIP)

## Overview

The World Cup Intelligence Platform (WCIP) is an end-to-end Data
Engineering and Business Intelligence project built using Python and
Power BI.

The project ingests football data from the API-Football REST API,
processes it through a multi-layer ETL pipeline (Raw → Bronze → Silver
→ Gold), and delivers interactive Power BI dashboards for team
performance analysis, player dependency analysis, and overall power
rankings.

The current prototype uses Premier League 2023 data to validate the
architecture before migrating to FIFA World Cup data. The project was
intentionally designed so the underlying pipeline and dashboard
architecture can be reused with future World Cup datasets.

---

## Project Status

**Current Status:** Prototype Complete ✅

The complete data pipeline, semantic model, and Power BI dashboards
have been built and validated using Premier League data.

The next milestone is migrating the project from Premier League data
to FIFA World Cup data while preserving the existing architecture.

---

## Architecture

```
                API-Football
                     │
                     ▼
              Raw JSON Layer
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
          Power BI Semantic Model
                     │
                     ▼
          Interactive Dashboards
```

---

## Technologies

- Python
- REST APIs
- JSON
- Power BI Desktop
- Power Query
- Data Modeling
- Git
- GitHub

---

## Project Structure

```
WCIP/

├── api-tests/
├── dashboards/
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docs/
├── planning/
├── scripts/
├── notebooks/
└── README.md
```

---

## Data Pipeline

### Raw Layer

Stores the original API responses without modification.

---

### Bronze Layer

Performs initial cleaning, field selection, and standardization while
preserving the source structure.

---

### Silver Layer

Applies business logic, aggregations, and intermediate calculations
used throughout the project.

---

### Gold Layer

Produces analytics-ready datasets consumed directly by Power BI.

Current Gold datasets include:

- Team Strength Index
- Player Dependency Score
- World Cup Power Rankings

---

## Power BI Semantic Model

The semantic model is built using a star schema.

Fact Tables:

- Team Strength
- Player Dependency
- Power Rankings

Dimension Tables:

- Dim Team

Relationships were created to support cross-filtering, slicers, and
interactive reporting across all dashboard pages.

---

## Dashboard Pages

### Executive Overview

Provides a high-level summary of the entire dataset, including:

- Teams analyzed
- Average Team Strength
- Average Power Score
- Highest Ranked Team
- Most Influential Player

---

### World Cup Power Rankings

Compares all teams using the custom World Cup Power Score.

Features include:

- Top 10 teams
- Ranking table
- Rank range slicer
- Team strength vs player dependency scatter plot

---

### Team Analysis

Allows users to analyze an individual team.

Includes:

- Team KPIs
- Team Strength Gauge
- Team Metrics Comparison
- Key Player Influence
- Team Summary Table

---

### Player Analysis

Provides player-level insights for a selected team.

Includes:

- Top Dependency Player
- Highest Dependency Score
- Goal Contributions vs Dependency Score
- Top 10 Most Influential Players
- Player Summary Table

---

### League Insights

Provides league-wide trends.

Includes:

- Highest Ranked Team
- Highest Power Score
- Team Strength vs Power Score
- League Power Rankings
- League Summary Table

---

## Features

- REST API data ingestion
- Multi-layer ETL pipeline
- Automated JSON processing
- Team Strength Index calculation
- Player Dependency Score calculation
- Custom Power Ranking algorithm
- Power BI semantic model
- Interactive filtering
- Team analysis
- Player analysis
- League insights

---

## Current Dataset

The current implementation uses Premier League 2023 data obtained from
the API-Football API.

This dataset serves as a prototype to validate the architecture before
migrating the pipeline to FIFA World Cup data.

Only the source data will change during migration. The overall
pipeline, semantic model, and dashboards are expected to remain
largely unchanged.

---

## Future Roadmap

### Phase 1 ✅

- Data Engineering Pipeline
- Bronze / Silver / Gold Architecture

### Phase 2 ✅

- Power BI Semantic Model
- Interactive Dashboards
- Documentation
- GitHub Repository

### Phase 3

- FIFA World Cup Data Migration

### Phase 4

- Power Score Normalization
- Model Refinement
- World Cup Score Validation

### Phase 5

- Final QA
- Portfolio Polish
- Resume Integration
- LinkedIn Showcase

---

## Results

Current prototype delivers:

- 20 Teams
- 1,000+ Players
- Multi-layer ETL pipeline
- Gold analytical datasets
- Power BI semantic model
- 5 interactive dashboard pages

---

## Repository

This repository contains:

- Python ETL pipeline
- Power BI dashboard (.pbix)
- Planning documents
- Design documentation
- Dashboard screenshots
- Source code

> **Note:** Power BI Desktop is currently only available on Windows. The `.pbix` file can be viewed by downloading it and opening it in Power BI Desktop.

---

## Author

**Mikel Nwankwor**

Rochester Institute of Technology

B.S. Computing & Information Technologies

Cybersecurity Minor
