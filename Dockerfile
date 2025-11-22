FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p artifacts

ENV BASE_URL="http://127.0.0.1:8000" \
    HEADLESS="true" \
    BROWSER="chromium"

CMD ["bash", "run_tests.sh"]
