import io
import math
import os
from pathlib import Path

import pytest
from PIL import Image

from tests.pages.home_page import HomePage

BASELINE_DIR = Path(__file__).parent.parent / "visual_baseline"


def _is_chromium_env() -> bool:
    """We only maintain visual baselines for Chromium in CI."""
    return os.getenv("BROWSER", "chromium").lower() == "chromium"


def _rmsdiff(img1: Image.Image, img2: Image.Image) -> float:
    """Compute an RMS pixel difference between two RGB images."""
    if img1.size != img2.size:
        raise ValueError(f"Image sizes differ: {img1.size} vs {img2.size}")

    h1 = img1.histogram()
    h2 = img2.histogram()

    if len(h1) != len(h2):
        raise ValueError("Image histograms differ in length.")

    squares = [(a - b) ** 2 for a, b in zip(h1, h2)]
    mean_square = sum(squares) / len(squares)
    return math.sqrt(mean_square)


def _compare_screenshot(page, baseline_name: str, *, full_page: bool = False, limit: float = 40.0):
    """
    Take a screenshot and compare it against a named baseline.

    `limit` is intentionally a bit generous for CI to tolerate minor differences
    (fonts, anti-aliasing), but it will still catch major layout changes.
    """
    # small wait to allow fonts/layout to stabilize
    page.wait_for_timeout(1000)

    screenshot_bytes = page.screenshot(full_page=full_page)
    baseline_path = BASELINE_DIR / baseline_name

    # First run: create baseline and skip comparison
    if not baseline_path.exists():
        baseline_path.write_bytes(screenshot_bytes)
        pytest.skip(f"Baseline image created at {baseline_path}. Re-run test to compare.")

    baseline_img = Image.open(baseline_path).convert("RGB")
    current_img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")

    assert baseline_img.size == current_img.size, (
        f"Screenshot size changed from {baseline_img.size} to {current_img.size}. "
        "If this is expected, update the baseline image."
    )

    diff = _rmsdiff(baseline_img, current_img)

    assert diff <= limit, (
        f"Visual regression detected for {baseline_name}: "
        f"RMS diff={diff:.2f} (limit={limit})"
    )


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.skipif(not _is_chromium_env(), reason="Visual regression only maintained for Chromium in CI")
def test_homepage_visual_regression(page, base_url):
    """Visual regression test for the main homepage view (Chromium only)."""
    home = HomePage(page, base_url)
    home.goto()
    # Homepage is usually a bit more variable between local/CI -> higher limit.
    _compare_screenshot(page, "homepage.png", full_page=False, limit=40.0)


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.skipif(not _is_chromium_env(), reason="Visual regression only maintained for Chromium in CI")
def test_products_section_visual_regression(page, base_url):
    """Visual regression test for the products section (Chromium only)."""
    home = HomePage(page, base_url)
    home.goto_products_section()
    # Products area is more stable.
    _compare_screenshot(page, "homepage_products.png", full_page=False, limit=20.0)
