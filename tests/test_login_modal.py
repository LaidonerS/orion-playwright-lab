from playwright.sync_api import Page


def test_login_flow_success(page: Page, base_url: str):
  page.goto(base_url + "#products")

  page.get_by_test_id("scenario-login").get_by_role("button", name="Open Login Modal").click()

  # Modal is visible
  modal = page.locator("#login-modal")
  modal.wait_for(state="visible")

  page.fill("#login-email", "qa@example.com")
  page.fill("#login-password", "test1234")

  page.get_by_test_id("login-submit").click()

  success = page.get_by_test_id("login-success")
  success.wait_for(state="visible")

  assert "Logged in as" in success.inner_text()
  assert "qa@example.com" in success.inner_text()
