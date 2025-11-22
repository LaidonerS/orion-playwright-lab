import os
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture(scope="session")
def playwright_instance():
  with sync_playwright() as p:
    yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
  headless = os.getenv("HEADLESS", "true").lower() == "true"
  browser = playwright_instance.chromium.launch(headless=headless, slow_mo=0 if headless else 250)
  yield browser
  browser.close()


@pytest.fixture
def page(browser):
  context = browser.new_context()
  page = context.new_page()
  yield page
  context.close()


@pytest.fixture
def base_url():
  return BASE_URL
