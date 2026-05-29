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


# --- 자동화 보류 (TC 시트 대시보드 나머지) — 사유별 그룹. 0 missing 유지용 ---
@requires_login
@pytest.mark.skip(reason="권한별(레벨2/4) 대시보드 접근/구성 = 해당 권한 계정 필요 (TC_146_002, TC_146_003, TC_146_004)")
def test_dashboard_access_by_level():
    ...


@requires_login
@pytest.mark.skip(reason="시스템 공지 표시/노출조건/이동 = 현재 환경 미표시, 공지 데이터 필요 (TC_147_001, TC_147_002, TC_147_003, TC_147_004, TC_147_005)")
def test_system_notice_detail():
    ...


@requires_login
@pytest.mark.skip(reason="가입 승인 대기 처리/페이지네이션/정렬/상세 = 대기 데이터 + 승인=파괴적 (TC_149_003, TC_149_006, TC_149_007, TC_149_009, TC_149_010, TC_150_001, TC_150_002, TC_150_003)")
def test_pending_signup_actions():
    ...


@requires_login
@pytest.mark.skip(reason="보정 만료 예정 필터/정렬/이동 = 데이터 필요 (TC_151_003, TC_151_004, TC_151_006, TC_151_007)")
def test_calibration_expiry_actions():
    ...


@requires_login
@pytest.mark.skip(reason="사용자 통계 그래프/세부 통계/다운로드 = 통계 데이터 + 다운로드 핸들링 (TC_152_002, TC_152_004, TC_152_005, TC_152_006, TC_152_007, TC_152_008, TC_152_009, TC_152_010, TC_152_012, TC_152_013, TC_153_001, TC_153_002)")
def test_user_statistics_detail():
    ...


@requires_login
@pytest.mark.skip(reason="데이터 기준 시점/새로고침/이상자 확인 = 데이터 + 파괴적 (TC_155_002, TC_155_004, TC_156_001)")
def test_data_reference_actions():
    ...


@requires_login
@pytest.mark.skip(reason="조치 필요 카드 표시/이동 = 데이터 필요 (TC_157_001, TC_158_001, TC_158_002, TC_158_003, TC_158_004)")
def test_action_required_cards():
    ...


@requires_login
@pytest.mark.skip(reason="전체 기술인 리스트 이동/데이터 = 데이터 필요 (TC_159_002, TC_159_003)")
def test_total_technician_list():
    ...


@requires_login
@pytest.mark.skip(reason="사용 현황 카드 = 데이터 필요 (TC_160_001, TC_160_002)")
def test_usage_status():
    ...
