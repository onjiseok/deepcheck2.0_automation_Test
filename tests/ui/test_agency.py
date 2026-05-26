"""소속업체 관리(/agency) 테스트.

level-3 계정으로 실측한 DOM(scripts/inspect_agency.py)에 맞춘 비파괴
표시/기본상태 검증. 협력사 등록/삭제, 승인 대기 처리는 데이터 변경이라 skip.
"""
import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.agency_page import AgencyPage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)


@pytest.fixture
def agency(logged_in_page) -> AgencyPage:
    return AgencyPage(logged_in_page).open()


@requires_login
@pytest.mark.smoke
def test_agency_loads(agency):
    expect(agency.heading).to_be_visible()


@requires_login
def test_sort_combobox_visible(agency):
    expect(agency.sort_combobox).to_be_visible()


@requires_login
def test_search_box_visible(agency):
    expect(agency.search_box).to_be_visible()


@requires_login
def test_approval_pending_disabled_by_default(agency):
    expect(agency.approval_pending_button).to_be_disabled()


@requires_login
def test_add_agency_button_enabled(agency):
    expect(agency.add_agency_button).to_be_enabled()


# --- 협력사 추가 다이얼로그 (열기만, 등록 안 함) ---
@requires_login
def test_add_dialog_opens_with_name_field(agency):
    agency.open_add_dialog()
    expect(agency.agency_name_field).to_be_visible()


@requires_login
def test_add_dialog_register_disabled_when_empty(agency):
    agency.open_add_dialog()
    expect(agency.register_button).to_be_disabled()


# --- 자동화 보류 (파괴적: 데이터 변경) ---
@requires_login
@pytest.mark.skip(reason="협력사 등록 = 실제 데이터 생성. 공유 환경 파괴적, 전용 데이터 필요")
def test_register_agency():
    ...


@requires_login
@pytest.mark.skip(reason="승인 대기 처리/협력사 삭제 = 데이터 변경. 전용 데이터 필요")
def test_approve_or_delete_agency():
    ...
