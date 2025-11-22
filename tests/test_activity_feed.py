import json

import pytest

from tests.pages.home_page import HomePage


def _fulfill_json(route, status, payload):
    route.fulfill(
        status=status,
        content_type="application/json",
        body=json.dumps(payload),
    )


@pytest.mark.ui
@pytest.mark.regression
def test_activity_feed_happy_path(page, base_url):
    home = HomePage(page, base_url)

    page.route(
        "**/api/activity",
        lambda route: _fulfill_json(
            route,
            200,
            [
                {"when": "Just now", "message": "New bug report from Orion client."},
                {"when": "5 min ago", "message": "Regression suite passed on main."},
            ],
        ),
    )

    home.goto_activity_section()
    home.activity_card.wait_for(state="visible")

    home.activity_load_button.click()

    home.activity_status.wait_for(state="visible")
    status_text = home.activity_status.inner_text()

    assert "Loaded 2 events" in status_text

    items = home.activity_items.all()
    assert len(items) == 2
    assert "New bug report" in items[0].inner_text()
    assert "Regression suite passed" in items[1].inner_text()


@pytest.mark.ui
@pytest.mark.regression
def test_activity_feed_empty_state(page, base_url):
    home = HomePage(page, base_url)

    page.route(
        "**/api/activity",
        lambda route: _fulfill_json(route, 200, []),
    )

    home.goto_activity_section()
    home.activity_load_button.click()

    home.activity_status.wait_for(state="visible")
    assert "No recent activity" in home.activity_status.inner_text()


@pytest.mark.ui
@pytest.mark.regression
def test_activity_feed_error_state(page, base_url):
    home = HomePage(page, base_url)

    page.route(
        "**/api/activity",
        lambda route: _fulfill_json(route, 500, {"error": "Something went wrong"}),
    )

    home.goto_activity_section()
    home.activity_load_button.click()

    home.activity_status.wait_for(state="visible")
    assert "Could not load activity" in home.activity_status.inner_text()
