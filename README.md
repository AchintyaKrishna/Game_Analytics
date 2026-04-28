# 🎾 Game Analytics — Unlocking Tennis Data with SportRadar API

> An end-to-end data engineering and analytics project that extracts live tennis data from the SportRadar API, structures it in a relational MySQL database, and surfaces insights through an interactive Streamlit dashboard.

---

## 📌 Project Overview

This project covers the **full analytics pipeline** — from raw API data to a polished, interactive web application:

| Phase | Title | Status |
|-------|-------|--------|
| 1 | Data Engineering — API Extraction & CSV Export | ✅ Complete |
| 2 | SQL Analytics — Schema Design & Queries | ✅ Complete |
| 3 | Streamlit Dashboard — Interactive Visualization | ✅ Complete |

**Data Source:** [SportRadar Tennis API v3](https://developer.sportradar.com/tennis/reference/tennis-v3)  
**Tech Stack:** Python · Pandas · MySQL · Plotly · Streamlit

---

## 📂 Project Structure

```
Game_Analytics/
│
├── api/
│   └── Tennis_Data_Pipeline.ipynb   # Data extraction, cleaning & CSV export
│
├── app/
│   └── app.py                       # Streamlit dashboard application
│
├── data/
│   ├── raw_data/                    # Raw JSON responses from the API
│   │   ├── live_competitions.json
│   │   ├── live_complexes.json
│   │   └── live_rankings.json
│   │
│   └── processed_data/              # Cleaned CSV files ready for SQL
│       ├── categories.csv
│       ├── competitions.csv
│       ├── complexes.csv
│       ├── venues.csv
│       ├── competitors.csv
│       └── rankings.csv
│
├── database/
│   ├── schema.sql                   # CREATE TABLE statements & relationships
│   ├── data_import.sql              # Data ingestion scripts
│   └── analysis_queries.sql         # 20+ analytical SQL queries
│
├── requirements.txt
├── game_analysis_doc.pdf            # Full project documentation
└── README.md
```

---

## ⚙️ Phase 1 — Data Engineering

### What It Does

The Jupyter Notebook (`api/Tennis_Data_Pipeline.ipynb`) is the core extraction engine. It:

1. **Fetches live data** from three SportRadar API v3 endpoints:
   - `GET /competitions.json` → Tournament & competition metadata
   - `GET /complexes.json` → Venue & complex information
   - `GET /double_competitors_rankings.json` → ATP Doubles rankings

2. **Backs up raw JSON** to `data/raw_data/` for reproducibility.

3. **Flattens nested JSON** into clean, relational Pandas DataFrames.

4. **Enforces data types** — ranking metrics (`rank`, `points`, `movement`) are cast to `int64`; missing values are handled for SQL compatibility.

5. **Exports 6 cleaned CSVs** to `data/processed_data/`.

### Running the Pipeline

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Open the notebook
jupyter notebook api/Tennis_Data_Pipeline.ipynb

# 3. Set your API key in the config cell, then Run All Cells
```

> **Note:** The processed CSVs are already included in the repo. You only need to re-run the notebook if you want to refresh with live data.

---

## 🗄️ Phase 2 — SQL Analytics

### Database Schema

The data is modelled as a **relational MySQL database** with 6 tables:

```
Categories ──< Competitions
Complexes  ──< Venues
Competitors ──< Rankings
```

**Entity Relationships:**

| Table | Primary Key | Foreign Key |
|-------|-------------|-------------|
| `Categories` | `category_id` | — |
| `Competitions` | `competition_id` | `category_id → Categories` |
| `Competitors` | `competitor_id` | — |
| `Rankings` | `rank_id` (auto) | `competitor_id → Competitors` |
| `Complexes` | `complex_id` | — |
| `Venues` | `venue_id` | `complex_id → Complexes` |

### Setting Up the Database

```sql
-- Step 1: Create schema
SOURCE database/schema.sql;

-- Step 2: Import data
SOURCE database/data_import.sql;

-- Step 3: Run analysis queries
SOURCE database/analysis_queries.sql;
```

### Key Analytical Queries

The `database/analysis_queries.sql` file contains **20+ queries** across three domains:

**🏟️ Competitions & Categories**
- Count competitions per category
- Identify parent/sub-competition hierarchies
- Filter competitions by type (`doubles`, `singles`) or gender

**🌍 Complexes & Venues**
- List venues per complex
- Find complexes with multiple venues
- Group venues by country or timezone

**🏅 Rankings & Competitors**
- Full leaderboard with rank and points
- Top 5 ranked competitors
- Competitors with stable rankings (no movement)
- Total points by country
- Find the highest-scoring competitor of the week

---

## 📊 Phase 3 — Streamlit Dashboard

### Dashboard Features

The interactive dashboard (`app/app.py`) gives users a **professional analytics interface** with three main views:

#### 📊 Global Analytics Tab
- **KPI Cards** — Total athletes, average points, countries represented, dominant region
- **Scatter Plot** — Points vs. Rank, sized by tournaments played (Viridis color scale)
- **Donut Chart** — Regional strength by player count (top 10 countries)
- **Bar Chart** — Cumulative points density by country (top 15)

#### 🏆 Top Performers Tab
- Full, filterable rankings leaderboard
- Color-coded movement indicators (🟢 rising / 🔴 falling / neutral)

#### 🔍 Player Deep Dive Tab
- Search any competitor by name
- **Profile Card** — rank, nationality, points, movement direction
- **Gauge Chart** — Points capacity relative to the global maximum

### Sidebar Filters (apply across all tabs)
- 🌍 **Country filter** — Focus on a single nation or view global data
- 🏆 **Rank range slider** — Narrow down to top-N players
- 🔥 **Points minimum slider** — Filter out lower-tier competitors

### Running the Dashboard

```bash
# From the project root
streamlit run app/app.py
```

The app will be available at **http://localhost:8501**

---

## 🚀 Quick Start (Full Stack)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Game_Analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Refresh data — skip if using existing CSVs
jupyter notebook api/Tennis_Data_Pipeline.ipynb

# 4. Set up the MySQL database
mysql -u root -p < database/schema.sql
mysql -u root -p tennis_db < database/data_import.sql

# 5. Launch the dashboard
streamlit run app/app.py
```

---

## 📦 Dependencies

```
requests       # API calls
pandas         # Data manipulation & CSV export
plotly         # Interactive charts
streamlit      # Web dashboard framework
mysql-connector # MySQL database connectivity
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 📄 Documentation

Full project documentation is available in [`game_analysis_doc.pdf`](./game_analysis_doc.pdf), covering the API integration design, data model decisions, and query rationale.

---

## 🏗️ Architecture Overview

```
SportRadar API v3
      │
      ▼
Tennis_Data_Pipeline.ipynb
  ├── Raw JSON  ──► data/raw_data/
  └── Cleaned CSVs ──► data/processed_data/
                              │
                              ▼
                       MySQL Database (tennis_db)
                         ├── schema.sql
                         └── analysis_queries.sql
                              │
                              ▼
                       Streamlit Dashboard (app.py)
                         ├── Global Analytics
                         ├── Top Performers
                         └── Player Deep Dive
```

---

## 📝 License

This project was built for educational and portfolio purposes using the SportRadar Trial API.

---

*Built with ❤️ using Python, MySQL, and Streamlit.*
