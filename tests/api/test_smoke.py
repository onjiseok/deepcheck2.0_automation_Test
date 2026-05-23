import pytest

from config.settings import settings

pytestmark = [pytest.mark.api, pytest.mark.smoke]


@pytest.mark.skipif(not settings.api_base_url, reason="API_BASE_URL not configured")
def test_health_endpoint(api):
    """Placeholder API smoke test: point at the real health/readiness route."""
    response = api.get("/health")
    assert response.status_code == 200
