from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from clients.api_client import ApiClient
from config.settings import settings
from pages.login_page import LoginPage
from reporting.influx_reporter import InfluxReporter

# Dev is a shared, sometimes-slow environment; give visibility/assertion checks
# headroom beyond the 5s default so late-rendering content doesn't flake.
expect.set_options(timeout=15000)

_reporter = InfluxReporter()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Used by pytest-playwright so page.goto('/path') resolves against the app."""
    return settings.base_url


@pytest.fixture
def api() -> ApiClient:
    client = ApiClient(base_url=settings.api_base_url)
    yield client
    client.close()


@pytest.fixture
def account():
    """Return a test account by permission level: account(3)."""
    return settings.account


@pytest.fixture(scope="session")
def auth_storage_state(browser, base_url):
    """Log in once (level 3) and capture the storage state for reuse."""
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).open().login(settings.account(3))
    page.wait_for_url(re.compile(r"/dashboard"), timeout=20000)
    state = context.storage_state()
    context.close()
    return state


@pytest.fixture
def logged_in_page(browser, base_url, auth_storage_state):
    """A page already authenticated as level 3, landed on the dashboard."""
    context = browser.new_context(base_url=base_url, storage_state=auth_storage_state)
    page = context.new_page()
    page.goto("/dashboard")
    yield page
    context.close()


def _suite_of(nodeid: str) -> str:
    if "tests/api" in nodeid:
        return "api"
    if "tests/ui" in nodeid:
        return "ui"
    return "other"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Record the test-body result, plus any setup failure (which masks the call).
    if report.when == "call" or (report.when == "setup" and report.failed):
        _reporter.record(
            nodeid=report.nodeid,
            outcome=report.outcome,
            duration=report.duration,
            suite=_suite_of(report.nodeid),
        )


def pytest_sessionfinish(session, exitstatus):
    _reporter.close()
