# Crypto ETL Pipeline

#### Video Demo:  https://www.youtube.com/watch?v=6XxWzAthxE4&feature=youtu.be

#### Description:

This project implements a simple ETL (Extract, Transform, Load) pipeline in Python. It retrieves cryptocurrency market data from an external API, processes the data, and stores it in a PostgreSQL database. The goal of the project is to demonstrate a basic but realistic data engineering workflow, including data ingestion, transformation, storage, logging, and execution from a Linux environment.

The pipeline follows three main steps. First, data is extracted from an API. Then, the raw data is transformed into a structured format suitable for relational storage. Finally, the data is loaded into a PostgreSQL table. Each run of the pipeline inserts a new snapshot of data, allowing the database to function as a simple time-series store.

The database schema is designed around a single table, `crypto_prices`, which stores price and market data along with a timestamp. A composite primary key `(coin_id, fetched_at)` ensures that each record is unique while allowing multiple observations over time. Financial values are stored using `NUMERIC` to avoid floating point precision issues.

The project can be executed manually or via a shell script, and is intended to run on a Linux server where it can be scheduled using tools like `cron`. Logging is included to track pipeline execution and verify that data is successfully inserted into the database.

## Project Files

* `etl_project.py`: Main Python script that runs the ETL pipeline (extract, transform, load).
* `run_elt.sh`: Shell script used to execute the pipeline, useful for automation (e.g. cron jobs).
* `sql_schema.psql`: SQL file defining the database schema, including the `crypto_prices` table.
* `.gitignore`: Specifies files and folders to ignore in version control.

## Design Choices

The project uses a single table instead of a normalized schema to keep the pipeline simple and easy to demonstrate. PostgreSQL was chosen over SQLite to better reflect real-world data engineering setups. The pipeline is structured to resemble a production workflow, even though it is implemented as a small standalone project.
