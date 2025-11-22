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

### 🎨 Visual regression testing

This project includes **visual regression tests** using Playwright screenshots + a simple image diff (Pillow):

- `tests/test_homepage_visual.py`
  - `test_homepage_visual_regression` – compares the main homepage view against `visual_baseline/homepage.png`
  - `test_products_section_visual_regression` – compares the products section against `visual_baseline/homepage_products.png`

How it works:

- On the **first run**, if a baseline image does not exist, the test:
  - Captures a screenshot
  - Saves it under `visual_baseline/`
  - Calls `pytest.skip(...)` to avoid failing
- On subsequent runs, the test:
  - Captures a fresh screenshot
  - Loads the corresponding baseline image
  - Computes an RMS pixel difference
  - Fails if the difference exceeds a threshold (`max_allowed_diff`)

Visual tests are **limited to Chromium** by design:

- CI sets `BROWSER=chromium|firefox|webkit`
- Visual tests call a helper that skips when `BROWSER != "chromium"`

This avoids false positives from small rendering differences between browsers, while still catching real UI changes in the primary target browser.
