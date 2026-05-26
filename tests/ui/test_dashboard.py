"""Dashboard tests, derived from TC sheet 'Deep check 2.0(웹) v1.0.0'.

Non-destructive display/landmark/default-state checks for a level-3 account,
verified against the live dashboard DOM. Data mutations (가입 승인/거절, 이상자
확인 삭제), file downloads, and graph/data-integrity checks are skipped pending
dedicated data fixtures.
"""
import re

import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.dashboard_page import DashboardPage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)


@pytest.fixture
def dashboard(logged_in_page) -> DashboardPage:
    return DashboardPage(logged_in_page)


# --- 사용자 권한 / 대시보드 진입 (TC_146_001) ---
@requires_login
@pytest.mark.smoke
def test_dashboard_loads_for_level3(dashboard):
    expect(dashboard.page).to_have_url(re.compile(r"/dashboard"))
    expect(dashboard.text("전체 기술인 수")).to_be_visible()


# --- 네비게이션바 항목 표시 ---
@requires_login
@pytest.mark.parametrize("name", DashboardPage.NAV_ITEMS)
def test_nav_items_visible(dashboard, name):
    expect(dashboard.nav_link(name).first).to_be_visible()


# --- Summary 파트1 카드 (TC_148_001) ---
@requires_login
def test_summary_cards_visible(dashboard):
    expect(dashboard.text("전체 기술인 수")).to_be_visible()
    expect(dashboard.text("전체 협력사 수")).to_be_visible()


# --- Summary 파트2: 측정/출근자 측정/이상자 현황 3카드 (TC_148_002) ---
@requires_login
def test_status_cards_visible(dashboard):
    expect(dashboard.text("측정 현황", exact=True)).to_be_visible()
    expect(dashboard.text("출근자 측정 현황")).to_be_visible()
    expect(dashboard.text("이상자 현황")).to_be_visible()


# --- 카드별 리스트 이동 링크 (TC_148_003 / TC_159_001) ---
@requires_login
@pytest.mark.parametrize(
    "name",
    [
        pytest.param("기술인 리스트", id="TC_159_001"),
        pytest.param("출근자 리스트", id="TC_148_003a"),
        pytest.param("이상자 리스트", id="TC_148_003b"),
    ],
)
def test_list_links_visible(dashboard, name):
    expect(dashboard.link(name)).to_be_visible()


# --- 데이터 기준 시점 표시 (TC_155_001) ---
@requires_login
def test_data_reference_timestamp_visible(dashboard):
    expect(dashboard.data_timestamp.first).to_be_visible()


# --- 사용자 통계 카드 (TC_152_001 / TC_152_003) ---
@requires_login
def test_user_statistics_card_visible(dashboard):
    expect(dashboard.text("사용자 통계")).to_be_visible()
    expect(dashboard.text("총 기술인 증감률")).to_be_visible()
    expect(dashboard.button("세부 통계 내역")).to_be_visible()


# --- 가입 승인 대기 카드 (TC_149_001) ---
@requires_login
def test_pending_signup_card_visible(dashboard):
    expect(dashboard.text("가입 승인 대기").first).to_be_visible()
    expect(dashboard.column_header("승인대기 신청일자")).to_be_visible()


# --- 가입 승인 대기: 표시 개수 디폴트 5개 (TC_149_008) ---
@requires_login
def test_pending_signup_default_page_size(dashboard):
    expect(dashboard.text("표시 개수")).to_be_visible()
    expect(dashboard.text("5개", exact=True).first).to_be_visible()


# --- 가입 승인 대기: 승인/거절/전체 버튼 디폴트 비활성화 (TC_149_005) ---
@requires_login
@pytest.mark.parametrize(
    "name,exact",
    [
        pytest.param("승인", True, id="TC_149_005a"),
        pytest.param("거절", True, id="TC_149_005b"),
        pytest.param("전체 가입 승인", False, id="TC_149_004"),
    ],
)
def test_pending_signup_buttons_disabled_by_default(dashboard, name, exact):
    expect(dashboard.button(name, exact=exact)).to_be_disabled()


# --- 보정 만료 예정 카드 (TC_151_001) ---
@requires_login
def test_calibration_expiry_card_visible(dashboard):
    expect(dashboard.text("보정 만료 예정").first).to_be_visible()
    expect(dashboard.column_header("보정 만료 예정일")).to_be_visible()


# --- 보정 만료 예정: 만료된 기술인 포함 토글 디폴트 ON (TC_151_005) ---
@requires_login
def test_calibration_expiry_toggle_default_on(dashboard):
    expect(dashboard.text("만료된 기술인 포함")).to_be_visible()
    expect(dashboard.expired_included_switch).to_be_checked()


# --- 보정 만료 예정: 보정 만료일 디폴트 7일 이내 (TC_151_002) ---
@requires_login
def test_calibration_expiry_default_filter(dashboard):
    expect(dashboard.text("보정 만료일")).to_be_visible()
    expect(dashboard.text("7일 이내")).to_be_visible()


# --- 현장 관리자 연락처 카드 (TC_154_001) ---
@requires_login
def test_site_manager_contacts_visible(dashboard):
    expect(dashboard.text("현장 관리자 연락처")).to_be_visible()
    expect(dashboard.column_header("전화번호")).to_be_visible()
    expect(dashboard.column_header("이메일")).to_be_visible()


# --- 자동화 보류 ---
@requires_login
@pytest.mark.skip(reason="시스템 공지 카드가 현재 환경 대시보드에 미표시(실측). 공지 데이터/노출조건 QA 확인 필요 (TC_147)")
def test_system_notice_card():
    ...


@requires_login
@pytest.mark.skip(reason="데이터 변경(승인/거절) = 공유 환경 파괴적. 전용 데이터 픽스처 필요 (TC_149_002~005)")
def test_approve_pending_signup():
    ...


@requires_login
@pytest.mark.skip(reason="이상자 리스트 확인/전체확인 = 데이터 삭제. 전용 데이터 필요 (TC_155_003/004)")
def test_confirm_abnormal_list():
    ...


@requires_login
@pytest.mark.skip(reason="PDF/Excel 다운로드 검증 = 데이터 의존. 다운로드 핸들링 별도 구현 (TC_152_011/012)")
def test_user_statistics_downloads():
    ...
