from playwright.sync_api import Page


class LoginModal:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open_products_section(self):
        self.page.goto(self.base_url + "#products")

    @property
    def open_modal_button(self):
        return self.page.get_by_test_id("scenario-login").get_by_role(
            "button", name="Open Login Modal"
        )

    @property
    def modal(self):
        return self.page.locator("#login-modal")

    @property
    def email_input(self):
        return self.page.locator("#login-email")

    @property
    def password_input(self):
        return self.page.locator("#login-password")

    @property
    def submit_button(self):
        return self.page.get_by_test_id("login-submit")

    @property
    def success_message(self):
        return self.page.get_by_test_id("login-success")

    # Actions
    def open(self):
        self.open_modal_button.click()
        self.modal.wait_for(state="visible")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
