def test_homepage_title_and_sections(page, base_url):
  page.goto(base_url)

  # Title
  assert "Orion Test Lab" in page.title()

  # Main heading
  heading = page.get_by_test_id("page-title")
  assert heading.is_visible()
  assert "QA Automation Playground" in heading.inner_text()

  # Navigation links
  for link_text in ["Dashboard", "Products", "Contact"]:
    link = page.get_by_role("link", name=link_text)
    assert link.is_visible()


def test_products_cards_present(page, base_url):
  page.goto(base_url + "#products")

  login_card = page.get_by_test_id("scenario-login")
  contact_card = page.get_by_test_id("scenario-contact")

  assert login_card.is_visible()
  assert "Login Flow" in login_card.inner_text()

  assert contact_card.is_visible()
  assert "Contact Form" in contact_card.inner_text()

  coming_soon_button = page.get_by_test_id("coming-soon-btn")
  assert coming_soon_button.is_disabled()
