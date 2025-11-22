# Orion Playwright Lab

A small demo web app + Playwright/pytest test suite designed for practising modern UI automation.

## Stack

- Static HTML/CSS/JS app served with `python -m http.server`
- Playwright (Python) + pytest
- GitHub Actions CI running Playwright tests on each push/PR

## Running locally

```bash
# 1. Activate venv
source venv/bin/activate

# 2. Start demo app in one terminal
cd app
python -m http.server 8000

# 3. In another terminal, run tests from project root
cd ..
export BASE_URL="http://127.0.0.1:8000"
export HEADLESS="false"  # set to true for headless
pytest -v
