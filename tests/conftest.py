import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

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
    browser_name = os.getenv("BROWSER", "chromium").lower()

    if browser_name == "firefox":
        browser = playwright_instance.firefox.launch(
            headless=headless,
            slow_mo=0 if headless else 200,
        )
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(
            headless=headless,
            slow_mo=0 if headless else 200,
        )
    else:
        # default to chromium
        browser = playwright_instance.chromium.launch(
            headless=headless,
            slow_mo=0 if headless else 200,
        )

    yield browser
    browser.close()


@pytest.fixture
def context(browser, request):
    context = browser.new_context(record_video_dir=str(VIDEOS_DIR))
    yield context
    context.close()


@pytest.fixture
def page(context, request):
    page = context.new_page()
    yield page

    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path))


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def base_url():
    return BASE_URL
