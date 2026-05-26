"""계정 관리(/account/site) 테스트.

level-3 계정으로 실측한 DOM(scripts/inspect_account.py)에 맞춘 비파괴
표시/기본상태 검증. 계정 생성(등록)/삭제/인증 재시도는 실제 계정 변경 +
인증 메일/알림 발송이라 파괴적이므로 skip한다.
"""
import re

import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.account_page import AccountPage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)


@pytest.fixture
def account_page(logged_in_page) -> AccountPage:
    return AccountPage(logged_in_page).open()


# --- 진입 / 서브 네비게이션 ---
@requires_login
@pytest.mark.smoke
def test_account_loads(account_page):
    expect(account_page.page).to_have_url(re.compile(r"/account/site"))
    expect(account_page.add_manager_button).to_be_visible()


@requires_login
@pytest.mark.parametrize("name", AccountPage.SUBNAV)
def test_subnav_links_visible(account_page, name):
    expect(account_page.subnav_link(name)).to_be_visible()


# --- 검색 / 필터 / 총 인원 ---
@requires_login
def test_search_box_visible(account_page):
    expect(account_page.search_box).to_be_visible()


@requires_login
def test_auth_filter_visible(account_page):
    expect(account_page.text("인증여부")).to_be_visible()


@requires_login
def test_total_count_visible(account_page):
    expect(account_page.total_count.first).to_be_visible()


# --- 액션 버튼 기본 상태 ---
@requires_login
def test_delete_disabled_by_default(account_page):
    expect(account_page.delete_button).to_be_disabled()


@requires_login
def test_add_manager_button_enabled(account_page):
    expect(account_page.add_manager_button).to_be_enabled()


# --- 목록 컬럼 ---
@requires_login
@pytest.mark.parametrize("name", AccountPage.LIST_COLUMNS)
def test_list_columns_visible(account_page, name):
    expect(account_page.column_header(name)).to_be_visible()


# --- 현장 관리자 추가 다이얼로그 (열기만, 등록 안 함) ---
@requires_login
def test_add_dialog_opens_with_fields(account_page):
    account_page.open_add_dialog()
    for field in AccountPage.ADD_FIELDS:
        expect(account_page.add_field(field)).to_be_visible()


@requires_login
def test_add_dialog_register_disabled_when_empty(account_page):
    account_page.open_add_dialog()
    expect(account_page.register_button).to_be_disabled()


# --- 자동화 보류 (파괴적: 계정 변경/메일·알림 발송) ---
@requires_login
@pytest.mark.skip(reason="현장 관리자 등록 = 실제 계정 생성 + 인증 메일 발송. 공유 환경 파괴적, 전용 데이터 필요")
def test_register_manager():
    ...


@requires_login
@pytest.mark.skip(reason="계정 삭제 = 공유 환경 파괴적. 전용 데이터/계정 필요")
def test_delete_manager():
    ...


@requires_login
@pytest.mark.skip(reason="인증 재시도 = 실제 인증 메일/알림 재발송. 파괴적, 전용 계정 필요")
def test_resend_verification():
    ...
