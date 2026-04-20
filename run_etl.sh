#!/bin/bash

set -e  # stop on error

# Absolute path to project
PROJECT_DIR="/Users/benjamincolding/cs50-python/etl-project"
# Absolute path to logs folder
LOGS_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOGS_DIR/etl.log"
# Use the correct Python interpreter (venv)
PYTHON="$PROJECT_DIR/.venv/bin/python"
LOCKFILE="/tmp/etl.lock"

# Prevent overlapping runs
if [ -f "$LOCKFILE" ]; then
    echo "$(date) - Job already running, exiting." >> "$LOG_FILE"
    exit 1
fi

touch "$LOCKFILE"

# Ensure lock is removed on exit
trap "rm -f $LOCKFILE" EXIT

mkdir -p "$LOGS_DIR"
cd "$PROJECT_DIR"


# Run ETL and append logs
$PYTHON etl_project.py >> "$LOG_FILE" 2>&1