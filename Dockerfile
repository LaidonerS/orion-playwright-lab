# Playwright Python base image (includes browsers + deps)
FROM mcr.microsoft.com/playwright/python:latest

# Workdir inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Ensure artifacts folder exists
RUN mkdir -p artifacts

# Default env vars (can be overridden)
ENV BASE_URL="http://127.0.0.1:8000" \
    HEADLESS="true" \
    BROWSER="chromium"

# Run our test runner
CMD ["bash", "run_tests.sh"]
