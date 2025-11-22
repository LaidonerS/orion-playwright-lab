import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

# Base URL (can be overridden with env)
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# Artifacts (screenshots, videos, HTML report, etc.)
ARTIFACTS_DIR = Path("artifacts")
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"

for d in (SCREENSHOTS_DIR, VIDEOS_DIR):
    d.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    browser = playwright_instance.chromium.launch(
        headless=headless,
        slow_mo=0 if headless else 200,
    )
    yield browser
    browser.close()


@pytest.fixture
def context(browser, request):
    """
    One browser context per test.
    We record video for each test here.
    """
    # record videos into VIDEOS_DIR
    context = browser.new_context(record_video_dir=str(VIDEOS_DIR))
    yield context
    context.close()


@pytest.fixture
def page(context, request):
    """
    Provides a fresh page for each test.
    If the test fails, we capture a screenshot.
    """
    page = context.new_page()
    yield page

    # after the test has run, check outcome
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path))


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to store the test phase reports on the item object,
    so fixtures can know if the test failed.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def base_url():
    return BASE_URL
