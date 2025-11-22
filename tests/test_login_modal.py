from tests.pages.login_modal import LoginModal


def test_login_flow_success(page, base_url):
    login = LoginModal(page, base_url)
    login.open_products_section()
    login.open()

    login.login("qa@example.com", "test1234")

    login.success_message.wait_for(state="visible")
    text = login.success_message.inner_text()

    assert "Logged in as" in text
    assert "qa@example.com" in text
