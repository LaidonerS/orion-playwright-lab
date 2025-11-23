#!/usr/bin/env bash
set -e

# Start simple HTTP server for demo app
cd /app/app
python -m http.server 8000 &
SERVER_PID=$!

# Give the server a moment to start
sleep 3

# Run tests from project root
cd /app

# Default envs (can be overridden at docker run)
export BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
export HEADLESS="${HEADLESS:-true}"
export BROWSER="${BROWSER:-chromium}"

mkdir -p artifacts

echo "Running tests with:"
echo "  BASE_URL=$BASE_URL"
echo "  HEADLESS=$HEADLESS"
echo "  BROWSER=$BROWSER"

python -m pytest --html=artifacts/report.html --self-contained-html -v

# Stop the server
kill "$SERVER_PID"
