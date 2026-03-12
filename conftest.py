"""
conftest.py — Pytest configuration for HTML report + automatic screenshots
"""

import pytest
import os
import base64
from datetime import datetime


# ─────────────── Create screenshots directory ───────────────
@pytest.fixture(scope="session", autouse=True)
def setup_dirs():
    os.makedirs("screenshots", exist_ok=True)


# ─────────────── Attach screenshot on failure ───────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Attach screenshot to HTML report
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_name = f"screenshots/{item.name}.png"
            try:
                driver.save_screenshot(screenshot_name)
                if os.path.exists(screenshot_name):
                    with open(screenshot_name, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode("utf-8")
                    extra = getattr(report, "extra", [])
                    extra.append(pytest.html.extras.image(
                        f"data:image/png;base64,{encoded}",
                        name=item.name
                    ))
                    report.extra = extra
            except Exception:
                pass


# ─────────────── Customize HTML Report Metadata ─────────────
def pytest_configure(config):
    config._metadata = {
        "Project": "Flipkart Search & Filter Module Testing",
        "Module": "Search & Product Filter",
        "Application URL": "https://www.flipkart.com/",
        "Tester": "QA Team",
        "Test Date": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
    }


def pytest_html_report_title(report):
    report.title = "Flipkart Test Report — Search & Product Filter Module"
