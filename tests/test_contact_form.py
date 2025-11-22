import pytest
from tests.pages.contact_page import ContactPage

@pytest.mark.smoke
@pytest.mark.ui
def test_contact_form_validation(page, base_url):
    contact = ContactPage(page, base_url)
    contact.goto()

    contact.submit_empty_form()

    for field_id in ["name", "email", "topic", "message"]:
        error = contact.error_for(field_id)
        assert error.inner_text() != ""

@pytest.mark.smoke
@pytest.mark.ui
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

@pytest.mark.regression
@pytest.mark.ui
def test_contact_form_with_random_data(page, base_url, faker):
    contact = ContactPage(page, base_url)
    contact.goto()

    name = faker.name()
    email = faker.email()
    message = faker.text(max_nb_chars=150)

    # try different topics over multiple runs in CI over time
    topic = "idea"

    contact.fill_form(
        name=name,
        email=email,
        topic=topic,
        message=message,
    )
    contact.submit()

    contact.success_message.wait_for(state="visible")
    assert "Thank you" in contact.success_message.inner_text()

@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "invalid_email",
    [
        "plainaddress",
        "missing-at-sign.com",
        "missing-domain@",
        pytest.param(
            "spaces in@email.com",
            marks=pytest.mark.xfail(reason="Current validator accepts spaces in email"),
        ),
        "missing-tld@domain",
    ],
)
def test_contact_form_invalid_email_validation(page, base_url, invalid_email, faker):
    contact = ContactPage(page, base_url)
    contact.goto()

    contact.fill_form(
        name=faker.name(),
        email=invalid_email,
        topic="bug",
        message=faker.text(max_nb_chars=80),
    )
    contact.submit()

    # We expect some error for the email field
    email_error = contact.error_for("email")
    assert email_error.inner_text() != ""
