from __future__ import annotations

import pathlib
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

# --- TC_ID 매핑 ----------------------------------------------------------
# 각 테스트 함수의 데코레이터+섹션 헤더 코멘트+본문에서 TC_xxx_xxx 패턴을 모아
# nodeid → TC_ID 목록 매핑을 만든다. 새 포인트의 tc_id 태그로 사용된다.
_TC_RE = re.compile(r"TC_\d{3}_\d{3}")
_TESTS_DIR = pathlib.Path(__file__).resolve().parent / "tests"


def _build_tc_map() -> dict[str, list[str]]:
    m: dict[str, list[str]] = {}
    if not _TESTS_DIR.exists():
        return m
    for py in _TESTS_DIR.rglob("*.py"):
        try:
            text = py.read_text(encoding="utf-8")
        except OSError:
            continue
        lines = text.splitlines(keepends=True)
        starts: list[tuple[int, str]] = []
        for i, line in enumerate(lines):
            mf = re.match(r"^def (test_\w+)", line)
            if not mf:
                continue
            # 데코레이터 + 바로 앞에 붙은 섹션 코멘트까지 거슬러 올라간다.
            # 빈 줄을 만나면 멈춰 → 다음 테스트의 헤더로 간주.
            start = i
            while start > 0:
                prev = lines[start - 1]
                if prev.strip() == "":
                    break
                stripped = prev.lstrip()
                if stripped.startswith("@") or stripped.startswith("#"):
                    start -= 1
                    continue
                break
            starts.append((start, mf.group(1)))
        for idx, (start, fname) in enumerate(starts):
            end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
            block = "".join(lines[start:end])
            ids = sorted(set(_TC_RE.findall(block)))
            key = f"{py.relative_to(_TESTS_DIR.parent).as_posix()}::{fname}"
            m[key] = ids
    return m


_TC_MAP = _build_tc_map()


def _tc_ids_for(nodeid: str) -> str:
    base = nodeid.split("[", 1)[0]
    ids = set(_TC_MAP.get(base, []))
    if "[" in nodeid:
        ids.update(_TC_RE.findall(nodeid[nodeid.index("["):]))
    return ", ".join(sorted(ids)) if ids else "(untagged)"


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
    # Skipped는 setup 단계에서 skipped=True로 보고된다 — failed와 함께 포함시켜
    # InfluxDB에 outcome="skipped"로 기록하고 TC별 결과 테이블에 노출시킨다.
    if report.when == "call" or (report.when == "setup" and (report.failed or report.skipped)):
        _reporter.record(
            nodeid=report.nodeid,
            outcome=report.outcome,
            duration=report.duration,
            suite=_suite_of(report.nodeid),
            tc_id=_tc_ids_for(report.nodeid),
        )


def pytest_sessionfinish(session, exitstatus):
    _reporter.close()
