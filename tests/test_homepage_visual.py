import io
import math
import os
from pathlib import Path

import pytest
from PIL import Image, ImageChops

from tests.pages.home_page import HomePage

BASELINE_DIR = Path("visual_baseline")
BASELINE_DIR.mkdir(exist_ok=True)


def _rmsdiff(img1: Image.Image, img2: Image.Image) -> float:
    """Root-mean-square difference between two images."""
    diff = ImageChops.difference(img1, img2)
    h = diff.histogram()
    sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
    sum_of_squares = float(sum(sq))
    rms = math.sqrt(sum_of_squares / (img1.size[0] * img1.size[1]))
    return rms


def _skip_if_not_chromium():
    browser_name = os.getenv("BROWSER", "chromium").lower()
    if browser_name != "chromium":
        pytest.skip(f"Visual regression tests only run on Chromium (current: {browser_name})")


def _compare_screenshot(page, baseline_name: str, *, full_page: bool = False, limit: float = 10.0):
    """Helper to take a screenshot and compare against a named baseline."""
    _skip_if_not_chromium()

    # small wait to allow fonts/layout to stabilize
    page.wait_for_timeout(1000)

    screenshot_bytes = page.screenshot(full_page=full_page)
    baseline_path = BASELINE_DIR / baseline_name

    # First run: create baseline and skip comparison
    if not baseline_path.exists():
        baseline_path.write_bytes(screenshot_bytes)
        pytest.skip(f"Baseline image created at {baseline_path}. Re-run test to compare.")

    from PIL import Image  # local import to avoid circular issues in some tools

    baseline_img = Image.open(baseline_path).convert("RGB")
    current_img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")

    assert baseline_img.size == current_img.size, (
        f"Screenshot size changed from {baseline_img.size} to {current_img.size}. "
        "If this is expected, update the baseline image."
    )

    diff = _rmsdiff(baseline_img, current_img)

    assert (
        diff <= limit
    ), f"Visual regression detected for {baseline_name}: RMS diff={diff:.2f} (limit={limit})"


@pytest.mark.ui
@pytest.mark.regression
def test_homepage_visual_regression(page, base_url):
    """Visual regression test for the main homepage view."""
    home = HomePage(page, base_url)
    home.goto()
    _compare_screenshot(page, "homepage.png", full_page=False)


@pytest.mark.ui
@pytest.mark.regression
def test_products_section_visual_regression(page, base_url):
    """Visual regression test for the products section."""
    home = HomePage(page, base_url)
    home.goto_products_section()
    _compare_screenshot(page, "homepage_products.png", full_page=False, limit=15.0)
