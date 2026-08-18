# World Cup Intelligence Platform

An end-to-end **data engineering and business intelligence platform** built with Python and Power BI that transforms football data from REST APIs into structured analytical models, custom performance metrics, and interactive dashboards.

The project demonstrates a complete analytics workflow using a **Bronze–Silver–Gold data architecture**, from API ingestion and transformation through analytical modeling and visualization.

![Executive Overview](docs/dashboard_screenshots/Executive%20Overview.png)

---

## Overview

The World Cup Intelligence Platform was developed to analyze international football data through an automated data pipeline and interactive reporting environment.

Python pipelines ingest data from **API-Football**, transform it through Bronze, Silver, and Gold layers, and produce analytics-ready datasets consumed by Power BI.

The platform provides analysis across teams and players while introducing custom analytical models including the **Team Strength Index, Player Dependency Score, and World Cup Power Score**.

---

## Features

- Automated REST API data ingestion
- Bronze, Silver, and Gold ETL architecture
- Data cleaning and transformation pipelines
- Custom team and player analytical models
- World Cup power rankings
- Executive tournament overview
- Team and player analysis
- Tournament leader analysis
- Interactive Power BI reporting
- DAX measures and semantic modeling

---

## Data Pipeline

```text
API-Football
      │
      ▼
Python Ingestion
      │
      ▼
  Raw Data
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
Interactive Dashboard
```

### Bronze Layer

Stores structured versions of the source API data while preserving the original information required for downstream processing.

### Silver Layer

Cleans, transforms, and combines Bronze datasets into analysis-ready team, player, standings, and match-performance data.

### Gold Layer

Produces business-ready analytical datasets and custom metrics used by the Power BI semantic model and dashboard.

---

## Analytical Models

### Team Strength Index

A custom metric designed to evaluate the overall strength of each national team using team and match-performance statistics.

### Player Dependency Score

Measures how heavily a national team relies on individual player contributions and identifies the most influential players within each team.

### World Cup Power Score

A composite analytical metric combining team performance and player influence to generate comparative national-team power rankings.

---

## Dashboard

The Power BI report contains five interactive analysis pages.

### Executive Overview

Provides a high-level view of the dataset, including team strength, power scores, leading nations, and influential players.

![Executive Overview](docs/dashboard_screenshots/Executive%20Overview.png)

### World Cup Power Rankings

Compares national teams using the custom World Cup Power Score, Team Strength Index, player dependency, and key-player metrics.

![Power Rankings](docs/dashboard_screenshots/Power%20Rankings.png)

### Team Analysis

Provides drill-down analysis for individual national teams, including team strength, power score, player dependency, key players, and comparative metrics.

![Team Analysis](docs/dashboard_screenshots/Team%20Analysis.png)

Additional dashboard pages include:

- **Player Analysis** — analyzes player contributions, dependency scores, and influence within each national team.
- **Tournament Leaders** — highlights leaders in goals, assists, goal contributions, and Player Dependency Score.

All dashboard screenshots are available in `docs/dashboard_screenshots/`.

The complete Power BI report is available at `dashboards/WCIP.pbix`.

---

## Repository Structure

```text
WCIP/
├── dashboards/
│   └── WCIP.pbix
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── dashboard_screenshots/
│   └── design/
│
├── scripts/
│   ├── API ingestion
│   ├── Bronze transformations
│   ├── Silver transformations
│   └── Gold analytical models
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Technology Stack

### Languages & Data
- Python
- JSON

### Data Engineering
- REST APIs
- API-Football
- ETL pipelines
- Bronze–Silver–Gold architecture

### Business Intelligence
- Microsoft Power BI
- Power Query
- DAX
- Semantic modeling

### Development
- Git
- GitHub
- Environment variables

---

## Running the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd WCIP
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Access

The ingestion scripts use an API-Football API key stored as an environment variable.

Create a `.env` file in the project root:

```text
API_FOOTBALL_KEY=your_api_key_here
```

The `.env` file is excluded from version control to prevent credentials from being committed.

### 4. Run the Data Pipelines

The Python scripts inside `scripts/` handle API ingestion and the transformations required to produce the Bronze, Silver, and Gold datasets.

The resulting Gold datasets provide the analytical layer used by the Power BI report.

---

## Project Status

**Completed — August 2026**

- REST API ingestion complete
- Bronze, Silver, and Gold pipelines complete
- Custom analytical models complete
- Power BI semantic model complete
- Interactive dashboard complete
- Project documentation complete

---

## Data & Project Disclaimer

This is an independent **data engineering and business intelligence portfolio project** built using football data available through API-Football.

The Team Strength Index, Player Dependency Score, World Cup Power Score, and associated rankings are custom analytical metrics developed specifically for this project. They should not be interpreted as official FIFA rankings, predictions, or official tournament results.

This project is not affiliated with or endorsed by FIFA.

---

## Author

**Mikel Nwankwor**

B.S. Computing & Information Technologies  
Cybersecurity Minor  
Rochester Institute of Technology