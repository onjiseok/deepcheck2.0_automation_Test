from __future__ import annotations

import pytest

from clients.api_client import ApiClient
from config.settings import settings
from reporting.influx_reporter import InfluxReporter

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
