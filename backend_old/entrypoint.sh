#!/bin/bash
set -e

# Configuration: Update these if your DB service name or port changes
DB_HOST="db"
DB_PORT="3306"

echo "Waiting for database at $DB_HOST:$DB_PORT..."

# This loop attempts to open a TCP connection to the DB
# If it fails, it sleeps for 2 seconds and tries again
until (echo > /dev/tcp/$DB_HOST/$DB_PORT) >/dev/null 2>&1; do
  echo "Database not ready yet... sleeping"
  sleep 2
done

echo "Database is ready! Starting application..."

# Exec ensures the Uvicorn process replaces the shell script as PID 1
# This is required for proper signal handling (like Ctrl+C)
exec uvicorn src.main:app --host 0.0.0.0 --port 8000