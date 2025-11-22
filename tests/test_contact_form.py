from tests.pages.contact_page import ContactPage


def test_contact_form_validation(page, base_url):
    contact = ContactPage(page, base_url)
    contact.goto()

    contact.submit_empty_form()

    for field_id in ["name", "email", "topic", "message"]:
        error = contact.error_for(field_id)
        assert error.inner_text() != ""


def test_contact_form_success(page, base_url):
    contact = ContactPage(page, base_url)
    contact.goto()

    contact.fill_form(
        name="Sten QA",
        email="sten@example.com",
        topic="idea",
        message="This is a test message for Playwright.",
    )
    contact.submit()

    contact.success_message.wait_for(state="visible")
    assert "Thank you" in contact.success_message.inner_text()
