from tests.pages.home_page import HomePage

@pytest.mark.smoke
@pytest.mark.ui
def test_homepage_title_and_sections(page, base_url):
    home = HomePage(page, base_url)
    home.goto()

    assert "Orion Test Lab" in page.title()
    assert home.heading.is_visible()
    assert "QA Automation Playground" in home.heading.inner_text()

    assert home.dashboard_link.is_visible()
    assert home.products_link.is_visible()
    assert home.contact_link.is_visible()

@pytest.mark.smoke
@pytest.mark.ui
def test_products_cards_present(page, base_url):
    home = HomePage(page, base_url)
    home.goto_products_section()

    login_card = page.get_by_test_id("scenario-login")
    contact_card = page.get_by_test_id("scenario-contact")

    assert login_card.is_visible()
    assert "Login Flow" in login_card.inner_text()

    assert contact_card.is_visible()
    assert "Contact Form" in contact_card.inner_text()

    coming_soon_button = page.get_by_test_id("coming-soon-btn")
    assert coming_soon_button.is_disabled()
