from playwright.sync_api import Page


def test_contact_form_validation(page: Page, base_url: str):
  page.goto(base_url + "#contact")

  # Click submit with empty form
  page.get_by_test_id("submit-contact").click()

  # Error messages should be visible
  for field_id in ["name", "email", "topic", "message"]:
    error = page.locator(f'[data-error-for="{field_id}"]')
    assert error.inner_text() != ""


def test_contact_form_success(page: Page, base_url: str):
  page.goto(base_url + "#contact")

  page.fill("#name", "Sten QA")
  page.fill("#email", "sten@example.com")
  page.select_option("#topic", "idea")
  page.fill("#message", "This is a test message for Playwright.")

  page.get_by_test_id("submit-contact").click()

  success = page.get_by_test_id("contact-success")
  success.wait_for(state="visible")

  assert "Thank you" in success.inner_text()
from playwright.sync_api import Page


def test_contact_form_validation(page: Page, base_url: str):
  page.goto(base_url + "#contact")

  # Click submit with empty form
  page.get_by_test_id("submit-contact").click()

  # Error messages should be visible
  for field_id in ["name", "email", "topic", "message"]:
    error = page.locator(f'[data-error-for="{field_id}"]')
    assert error.inner_text() != ""


def test_contact_form_success(page: Page, base_url: str):
  page.goto(base_url + "#contact")

  page.fill("#name", "Sten QA")
  page.fill("#email", "sten@example.com")
  page.select_option("#topic", "idea")
  page.fill("#message", "This is a test message for Playwright.")

  page.get_by_test_id("submit-contact").click()

  success = page.get_by_test_id("contact-success")
  success.wait_for(state="visible")

  assert "Thank you" in success.inner_text()
