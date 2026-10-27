# Weather Data Pipeline

An end-to-end data engineering project that collects historical weather data for **Porto, Lisbon, and Madrid**, preserves the original API responses, transforms and validates the data, stores it in **Parquet**, and runs analytical queries using **DuckDB and SQL**.

## Problem

Historical weather data is useful for comparing conditions across cities and dates, but API responses are not always in a format suitable for analysis.

This project builds a small, reproducible ETL pipeline that turns hourly weather observations from the [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) into a consistent dataset that can be queried with SQL.

The current dataset covers **September 1–2, 2026**, at hourly resolution, in **UTC**: **48 observations per city, 144 in total**.

## Architecture

```text
Open-Meteo Historical Weather API
                |
                v
       Extract (Requests)
                |
                v
    Raw JSON (one file per city)
                |
                v
   Transform + Validate (Pandas)
                |
                v
       Load (PyArrow)
                |
                v
     Processed weather.parquet
                |
                v
       DuckDB + SQL Analytics
```

The original JSON responses are kept separate from the processed data, so transformations can be rerun without changing the raw source files. The `main.py` entry point runs extraction, transformation/loading, and analytics in order.

## Tech Stack

| Technology        | Purpose                               |
|-------------------|---------------------------------------|
| Python 3.12       | Pipeline implementation               |
| Requests          | HTTP requests to the weather API      |
| Pandas            | Data transformation and validation    |
| PyArrow / Parquet | Columnar storage of processed data    |
| DuckDB + SQL      | Analytics directly over Parquet       |
| pytest            | Automated data quality tests          |
| uv                | Dependency installation and lock file |

## Project Structure

```text
weather-data-pipeline/
├── analysis/
│   ├── queries.sql          # Four SQL analyses
│   └── run_queries.py       # Execute SQL queries with DuckDB
├── data/
│   ├── raw/                 # Generated API responses (JSON)
│   └── processed/           # Generated weather.parquet
├── src/
│   ├── extract.py           # Fetch and save raw weather data
│   ├── transform.py         # Transform and validate observations
│   └── load.py              # Write and verify Parquet output
├── tests/
│   └── test_transform.py    # Data quality tests
├── main.py                  # Run the complete pipeline
├── requirements.txt
├── requirements-lock.txt
├── .gitignore
├── LICENSE
└── README.md
```

The `data/` outputs and local virtual environment are generated during execution and are not tracked in Git.

## How to Run

The commands below are for **Linux / WSL**, using Python 3.12 and [`uv`](https://docs.astral.sh/uv/).

**1. Clone the repository**

```bash
git clone https://github.com/GustavoFerreira24/weather-data-pipeline.git
cd weather-data-pipeline
```

**2. Create a virtual environment and install dependencies**

```bash
uv venv --python 3.12
uv pip sync --python .venv/bin/python requirements-lock.txt
```

**3. Run the full pipeline**

```bash
.venv/bin/python main.py
```

This command fetches the weather data, creates the raw JSON files, validates and writes the Parquet dataset, and prints the SQL analysis results.

**4. Run automated tests**

```bash
.venv/bin/python -m pytest -v
```

You can also run individual stages:

```bash
.venv/bin/python src/extract.py
.venv/bin/python src/load.py
.venv/bin/python analysis/run_queries.py
```

Run the extraction and load stages before the analytics stage if the generated data does not exist yet.

## Data Model and Data Quality

The processed dataset contains one row per **city and UTC hour**:

| Column          | Meaning                                       |
|-----------------|-----------------------------------------------|
| `city`          | City identifier (`porto`, `lisboa`, `madrid`) |
| `timestamp`     | Hourly observation time (UTC)                 |
| `temperature`   | Temperature (°C)                              |
| `humidity`      | Relative humidity (%)                         |
| `precipitation` | Hourly precipitation (mm)                     |
| `wind_speed`    | Wind speed (km/h)                             |

Before writing Parquet, the pipeline:

- Checks the expected columns and converts numeric fields to numeric types.
- Parses timestamps as timezone-aware UTC datetimes.
- Rejects missing city or timestamp values; keeps missing weather measurements as nulls instead of inventing values.
- Rejects humidity outside **0–100%**, negative precipitation, and negative wind speeds.
- Removes fully identical rows and rejects conflicting records with the same **city + timestamp**.

The automated tests cover invalid humidity, conflicting observations, and removal of identical duplicates.

## SQL Analytics and Results

DuckDB queries the Parquet file directly using `read_parquet()`, without importing it into a separate database. The queries in `analysis/queries.sql` provide:

1. Average temperature by city.
2. Average daily temperature by city.
3. Daily total precipitation and number of recorded precipitation hours.
4. Daily minimum, maximum, and temperature range by city.

### Example results (September 1–2, 2026, UTC)

**Average temperature by city**

| City   | Average temperature (°C) |
|--------|-------------------------:|
| Madrid |                    27.70 |
| Lisbon |                    22.61 |
| Porto  |                    19.33 |

**Largest daily temperature ranges**

| City   | Date (UTC) | Minimum (°C) | Maximum (°C) | Range (°C) |
|--------|------------|-------------:|-------------:|-----------:|
| Madrid | 2026-09-02 |         18.7 |         35.3 |       16.6 |
| Lisbon | 2026-09-02 |         17.4 |         32.1 |       14.7 |
| Madrid | 2026-09-01 |         19.7 |         34.2 |       14.5 |

For this two-day sample, the daily precipitation totals were **0.0 mm** across the three cities, with **24 recorded hours per city per day**.

These results describe the fixed historical sample used in this project, not current weather conditions.

## What I Learned

- How to design and connect the **Extract → Transform → Load** stages of a small pipeline.
- Why preserving raw API responses is useful for reproducibility and debugging.
- How to turn nested JSON data into a consistent tabular schema with Pandas.
- How to implement data quality rules and test edge cases with pytest.
- Why timezone handling matters when aggregating timestamped data by day.
- How Parquet supports efficient analytical storage and how DuckDB queries it directly with SQL.
- How to make a project reproducible with a dependency lock file and a single entry point.

## Scope and Limitations

This is a **learning-focused mini project**, not a production ingestion platform. It currently uses a fixed historical date range, three cities, and simple local files. Potential next steps include configurable date ranges, request retries/logging, larger datasets, and additional data quality tests.