import pytest

from config.settings import settings

pytestmark = [pytest.mark.ui, pytest.mark.smoke]


@pytest.mark.skipif(not settings.base_url, reason="BASE_URL not configured")
def test_home_page_loads(page):
    """Placeholder smoke test: replace assertion with a real landmark of the app."""
    page.goto("/")
    assert page.title() != ""
