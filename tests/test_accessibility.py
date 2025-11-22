import json
from textwrap import indent

import pytest

from tests.pages.home_page import HomePage

A11Y_SEVERITIES = {"serious", "critical"}
AXE_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"


def _inject_axe(page):
    # Only inject if not already present
    page.add_script_tag(url=AXE_CDN_URL)
    has_axe = page.evaluate("typeof axe !== 'undefined'")
    assert has_axe, "axe-core failed to load into the page"


def _run_axe(page):
    _inject_axe(page)
    # Run axe in the browser context
    result = page.evaluate(
        """async () => {
            return await axe.run(document, {
                resultTypes: ['violations'],
            });
        }"""
    )
    return result


def _format_violations(violations):
    lines = []
    for v in violations:
        lines.append(f"- [{v.get('impact', 'none')}] {v.get('id')} – {v.get('description')}")
        # Include a couple of sample nodes for context
        for node in v.get("nodes", [])[:2]:
            target = ", ".join(node.get("target", []))
            snippet = node.get("html", "").strip().replace("\n", " ")
            lines.append(
                indent(
                    f"target: {target or '(no target)'}\n"
                    f"snippet: {snippet[:200]}",
                    prefix="    ",
                )
            )
    return "\n".join(lines)


@pytest.mark.a11y
@pytest.mark.ui
@pytest.mark.regression
def test_homepage_has_no_serious_accessibility_violations(page, base_url):
    """
    Basic axe-core accessibility audit for the homepage.

    Fails only on 'serious' and 'critical' issues to avoid noise,
    while still catching important problems.
    """
    home = HomePage(page, base_url)
    home.goto()

    result = _run_axe(page)
    violations = result.get("violations", [])

    serious_violations = [
        v for v in violations if v.get("impact") in A11Y_SEVERITIES
    ]

    if serious_violations:
        msg = _format_violations(serious_violations)
        pytest.fail(
            f"Accessibility violations found (serious/critical): {len(serious_violations)}\n\n{msg}"
        )
