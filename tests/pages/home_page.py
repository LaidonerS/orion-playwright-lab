from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    # Navigation
    def goto(self):
        self.page.goto(self.base_url)

    # Elements
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

    # Sections
    def goto_products_section(self):
        self.page.goto(self.base_url + "#products")

    def goto_contact_section(self):
        self.page.goto(self.base_url + "#contact")
