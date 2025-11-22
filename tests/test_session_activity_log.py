
import pytest

from tests.pages.home_page import HomePage
from tests.pages.contact_page import ContactPage
from tests.pages.login_modal import LoginModal


@pytest.mark.ui
@pytest.mark.regression
def test_session_activity_initial_state(page, base_url):
    """Session log should show a friendly empty state initially."""
    home = HomePage(page, base_url)
    home.goto_activity_section()

    home.session_activity_list.wait_for(state="visible")
    text = home.session_activity_list.inner_text()
    assert "No interactions yet" in text


@pytest.mark.ui
@pytest.mark.regression
def test_session_activity_logs_login_success(page, base_url):
    """Login success should add an entry to the session activity log."""
    home = HomePage(page, base_url)
    home.goto()

    login = LoginModal(page, base_url)
    login.open()

    # Use non-empty demo credentials (the demo app typically treats non-empty as "success").
    # If your test_login_flow_success uses different values, you can copy them here.
    login.login("qa@example.com", "playwright123")

    home.goto_activity_section()
    home.session_activity_list.wait_for(state="visible")

    items = home.session_activity_items.all()
    assert len(items) >= 1

    first_text = items[0].inner_text()
    # This matches the text we configured in index.html: "Login success for <email>"
    assert "Login success" in first_text


@pytest.mark.ui
@pytest.mark.regression
def test_session_activity_logs_contact_submission(page, base_url):
    """Contact form success should add an entry to the session activity log."""
    contact = ContactPage(page, base_url)
    contact.goto()

    contact.fill_form(
        name="Session Log Tester",
        email="tester@example.com",
        topic="idea",
        message="Testing session log integration.",
    )
    contact.submit()

    home = HomePage(page, base_url)
    home.goto_activity_section()
    home.session_activity_list.wait_for(state="visible")

    items = home.session_activity_items.all()
    # This matches the text we configured in index.html: "Contact form submitted (topic)"
    assert any("Contact form submitted" in item.inner_text() for item in items)
