#!/bin/bash

set -e

PROJECT_DIR="/home/benjamin/ETL-pipeline"
LOGS_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOGS_DIR/etl.log"
PYTHON="$PROJECT_DIR/.venv/bin/python"
LOCKFILE="/tmp/etl.lock"

if [ -f "$LOCKFILE" ]; then
    echo "$(date) - Job already running, exiting." >> "$LOG_FILE"
    exit 1
fi

touch "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

mkdir -p "$LOGS_DIR"
cd "$PROJECT_DIR"

"$PYTHON" etl_project.py >> "$LOG_FILE" 2>&1