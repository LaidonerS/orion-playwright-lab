from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    # Navigation
    def goto(self):
        self.page.goto(self.base_url)

    def goto_products_section(self):
        self.page.goto(self.base_url + "#products")

    def goto_contact_section(self):
        self.page.goto(self.base_url + "#contact")

    def goto_activity_section(self):
        self.page.goto(self.base_url + "#activity")

    # Top-level elements
    @property
    def heading(self):
        return self.page.get_by_test_id("page-title")

    @property
    def dashboard_link(self):
        return self.page.get_by_role("link", name="Dashboard")

    @property
    def products_link(self):
        return self.page.get_by_role("link", name="Products")

    @property
    def contact_link(self):
        return self.page.get_by_role("link", name="Contact")

    # Activity feed (remote API)
    @property
    def activity_card(self):
        return self.page.get_by_test_id("scenario-activity")

    @property
    def activity_load_button(self):
        return self.page.get_by_test_id("load-activity")

    @property
    def activity_status(self):
        return self.page.get_by_test_id("activity-status")

    @property
    def activity_items(self):
        return self.page.get_by_test_id("activity-item")

    # Session activity log
    @property
    def session_activity_list(self):
        return self.page.get_by_test_id("session-activity-list")

    @property
    def session_activity_items(self):
        return self.page.get_by_test_id("session-activity-item")
