import io
import math
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


@pytest.mark.ui
@pytest.mark.regression
def test_homepage_visual_regression(page, base_url):
    """Visual regression test for the main homepage view."""
    home = HomePage(page, base_url)
    home.goto()

    # small wait to allow fonts/layout to stabilize
    page.wait_for_timeout(1000)

    # current screenshot as bytes (viewport only, not full page)
    screenshot_bytes = page.screenshot(full_page=False)

    baseline_path = BASELINE_DIR / "homepage.png"

    # First run: create baseline and skip comparison
    if not baseline_path.exists():
        baseline_path.write_bytes(screenshot_bytes)
        pytest.skip("Baseline image created at visual_baseline/homepage.png. Re-run test to compare.")

    # Load baseline & current as Pillow images
    baseline_img = Image.open(baseline_path).convert("RGB")
    current_img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")

    assert baseline_img.size == current_img.size, (
        f"Screenshot size changed from {baseline_img.size} to {current_img.size}. "
        "If this is expected, update the baseline."
    )

    diff = _rmsdiff(baseline_img, current_img)
    # Tweak threshold if needed (depends how strict you want to be)
    max_allowed_diff = 5.0

    assert (
        diff <= max_allowed_diff
    ), f"Visual regression detected: RMS diff={diff:.2f} (limit={max_allowed_diff})"
