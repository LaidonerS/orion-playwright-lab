# Orion Playwright Lab

Orion Playwright Lab is a small demo web app + Playwright/Python test framework, built to showcase modern QA automation practices:

- Page Object Model (POM)
- Cross-browser UI testing (Chromium, Firefox, WebKit)
- Pytest + HTML reports + test artifacts (screenshots, videos)
- GitHub Actions CI (with 30-day artifact retention)
- Dockerized test execution
- Data-driven & negative tests using Faker + parametrization

---

## 🔧 Tech stack

- **Language:** Python 3.x
- **Test runner:** Pytest
- **UI automation:** Playwright (sync API)
- **Reporting:** pytest-html (self-contained HTML report)
- **Random test data:** Faker / pytest-faker
- **Containerization:** Docker (Playwright base image)
- **CI:** GitHub Actions (3-browser matrix)

---

## 📁 Project structure

```text
orion-playwright-lab/
  app/                      # Static demo web app (Orion Test Lab UI)
  tests/
    pages/                  # Page Object Model classes
      home_page.py
      contact_page.py
      login_modal.py
    test_homepage.py        # Homepage & navigation tests
    test_contact_form.py    # Contact form validation + Faker tests
    test_login_modal.py     # Login flow tests
    conftest.py             # Playwright fixtures, browser/context/page, artifacts
  artifacts/                # Test outputs (HTML report, screenshots, videos) [gitignored]
  .github/
    workflows/
      tests.yml             # CI: cross-browser test matrix + artifacts
  Dockerfile                # Dockerized test runner
  run_tests.sh              # Starts demo server + runs pytest inside container
  requirements.txt
  pytest.ini
  README.md
