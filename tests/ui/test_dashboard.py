"""Dashboard tests, derived from TC sheet 'Deep check 2.0(웹) v1.0.0'.

Covers non-destructive display/landmark checks for a level-3 account. Data
mutations (가입 승인/거절, 이상자 확인 삭제), file downloads, and graph/data-integrity
checks are skipped pending dedicated data fixtures and a verification run.
Card titles beyond the confirmed Summary landmarks are inferred from the spec.
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


# --- 사용자 권한 / 대시보드 진입 (TC_146_001, TC_146_004) ---
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


# --- Summary 카드 표시 (TC_148_001 / TC_148_002) ---
@requires_login
def test_summary_cards_visible(dashboard):  # TC_148_001
    expect(dashboard.text("전체 기술인 수")).to_be_visible()
    expect(dashboard.text("전체 협력사 수")).to_be_visible()


@requires_login
def test_measurement_status_visible(dashboard):  # TC_148_002
    expect(dashboard.text("측정 현황")).to_be_visible()
    expect(dashboard.text("총 측정자 수")).to_be_visible()


# --- 데이터 기준 시점 표시 (TC_155_001) ---
@requires_login
def test_data_reference_timestamp_visible(dashboard):
    expect(dashboard.data_timestamp.first).to_be_visible()


# --- 카드 표시 (스펙 기반 추정 제목 - 검증 런으로 확정 필요) ---
INFERRED_CARDS = [
    pytest.param("시스템 공지", id="TC_147_001"),
    pytest.param("가입 승인 대기", id="TC_149_001"),
    pytest.param("보정 만료 예정", id="TC_151_001"),
    pytest.param("사용자 통계", id="TC_152_001"),
]


@requires_login
@pytest.mark.parametrize("title", INFERRED_CARDS)
def test_inferred_card_visible(dashboard, title):
    expect(dashboard.text(title).first).to_be_visible()


# --- 자동화 보류 (전용 데이터/파괴적/다운로드) ---
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
