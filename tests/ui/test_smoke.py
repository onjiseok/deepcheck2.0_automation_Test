import pytest
from playwright.sync_api import expect

from config.settings import settings

pytestmark = [pytest.mark.ui, pytest.mark.smoke]


@pytest.mark.skipif(not settings.base_url, reason="BASE_URL not configured")
def test_login_page_reachable(page):
    """Smoke: the app serves its login screen (entry-point landmark)."""
    page.goto("/login")
    expect(page.get_by_role("textbox", name="이메일")).to_be_visible()
