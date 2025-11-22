from playwright.sync_api import Page


class ContactPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self):
        self.page.goto(self.base_url + "#contact")

    # Locators
    @property
    def name_input(self):
        return self.page.locator("#name")

    @property
    def email_input(self):
        return self.page.locator("#email")

    @property
    def topic_select(self):
        return self.page.locator("#topic")

    @property
    def message_textarea(self):
        return self.page.locator("#message")

    @property
    def submit_button(self):
        return self.page.get_by_test_id("submit-contact")

    @property
    def success_message(self):
        return self.page.get_by_test_id("contact-success")

    def error_for(self, field_id: str):
        return self.page.locator(f'[data-error-for="{field_id}"]')

    # Actions
    def submit_empty_form(self):
        self.submit_button.click()

    def fill_form(self, name: str, email: str, topic: str, message: str):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.topic_select.select_option(topic)
        self.message_textarea.fill(message)

    def submit(self):
        self.submit_button.click()
from playwright.sync_api import Page


class ContactPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self):
        self.page.goto(self.base_url + "#contact")

    # Locators
    @property
    def name_input(self):
        return self.page.locator("#name")

    @property
    def email_input(self):
        return self.page.locator("#email")

    @property
    def topic_select(self):
        return self.page.locator("#topic")

    @property
    def message_textarea(self):
        return self.page.locator("#message")

    @property
    def submit_button(self):
        return self.page.get_by_test_id("submit-contact")

    @property
    def success_message(self):
        return self.page.get_by_test_id("contact-success")

    def error_for(self, field_id: str):
        return self.page.locator(f'[data-error-for="{field_id}"]')

    # Actions
    def submit_empty_form(self):
        self.submit_button.click()

    def fill_form(self, name: str, email: str, topic: str, message: str):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.topic_select.select_option(topic)
        self.message_textarea.fill(message)

    def submit(self):
        self.submit_button.click()
