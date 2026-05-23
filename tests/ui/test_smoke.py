import pytest

from config.settings import settings
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.smoke]


@pytest.mark.skipif(not settings.base_url, reason="BASE_URL not configured")
def test_home_page_loads(page):
    """Placeholder smoke test: replace assertion with a real landmark of the app."""
    page.goto("/")
    assert page.title() != ""


@pytest.mark.skipif(3 not in settings.accounts, reason="level-3 account not configured")
def test_login_level3(page, account):
    """Example login flow. Replace the post-login assertion with a real one."""
    LoginPage(page).open().login(account(3))
    # TODO: assert a logged-in landmark once the dashboard markup is known.
    assert "/login" not in page.url
