# Crypto ETL Pipeline

## Overview

This project implements a small, production-inspired ETL pipeline in Python. It ingests cryptocurrency market data from an external API, transforms it into a structured format, and persists it in a PostgreSQL database.

The goal is to demonstrate core data engineering concepts: reproducible data ingestion, transformation, storage, logging, and scheduled execution in a Linux environment.

---

## Architecture

The pipeline follows a standard ETL design:

* **Extract**: Fetch cryptocurrency data from the CoinMarketCap API
* **Transform**: Clean and normalize nested JSON into a tabular structure
* **Load**: Insert data into PostgreSQL

Each execution inserts a new snapshot, making the dataset suitable for **time-series analysis**.

Execution flow:

1. API request is made with authentication
2. Data is transformed into a list of structured records
3. Records are inserted into the database
4. Execution is logged for traceability

---

## Database Design

The pipeline writes to a single table:

`crypto_prices`

Key design decisions:

* **Composite primary key**: `(coin_id, fetched_at)`
  Ensures uniqueness while allowing multiple observations over time
* **Time-series structure**: Each run represents a snapshot
* **NUMERIC data types**: Used for financial values to avoid floating-point precision issues

This design prioritizes simplicity while still supporting historical analysis.

---

## Execution & Automation

The pipeline can be executed:

* Manually via:

  ```bash
  python project.py
  ```
* Or via a shell script (`run_etl.sh`)
* And scheduled using **cron** on a Linux server

Logging is implemented using Python’s `logging` module and written to:

```
logs/etl.log
```

This enables basic monitoring and debugging of pipeline runs.

---

## Project Structure

* `project.py`
  Main entry point containing the ETL pipeline logic

* `test_project.py`
  Pytest-based unit tests for core functions

* `requirements.txt`
  Python dependencies for reproducibility

* `sql_schema.psql`
  SQL schema defining the `crypto_prices` table

* `run_etl.sh`
  Helper script for running the pipeline (e.g. via cron)

* `.gitignore`
  Excludes environment-specific files (`.env`, logs, virtual environment)

---

## Design Considerations

* **Denormalized schema**
  Coin metadata is stored alongside observations to simplify the pipeline. In a production setting, this would likely be normalized.

* **PostgreSQL over SQLite**
  Chosen to reflect real-world usage and enable scalable storage.

* **Environment-based configuration**
  API keys and database credentials are stored in a `.env` file (not committed), following best practices.

* **Reproducibility**
  The project can be recreated from scratch using `requirements.txt` and the SQL schema.

---

## Potential Improvements

* Incremental loading instead of full snapshots
* Retry logic and error handling for API failures
* Data validation layer before insertion
* Table partitioning for large-scale time-series data
* Integration with a BI tool or dashboard

---

## Summary

This project demonstrates the fundamental components of a data pipeline in a clear and reproducible way. While intentionally simple, it reflects patterns used in real-world data engineering systems and serves as a foundation for more advanced workflows.
