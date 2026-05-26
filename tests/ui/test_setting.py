"""설정(/setting/basic) 테스트.

level-3 계정으로 실측한 DOM(scripts/inspect_setting.py)에 맞춘 비파괴
표시/기본상태 검증. 설정 변경 저장(저장 버튼 클릭), 항목 추가/삭제는 공유
환경에 영향을 주므로 skip한다.
"""
import re

import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.setting_page import SettingPage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)


@pytest.fixture
def setting(logged_in_page) -> SettingPage:
    return SettingPage(logged_in_page).open()


# --- 진입 / 서브 네비게이션 ---
@requires_login
@pytest.mark.smoke
def test_setting_loads(setting):
    expect(setting.page).to_have_url(re.compile(r"/setting"))
    expect(setting.subnav_link("기본 설정")).to_be_visible()


@requires_login
@pytest.mark.parametrize("name", SettingPage.SUBNAV)
def test_subnav_links_visible(setting, name):
    expect(setting.subnav_link(name)).to_be_visible()


# --- 토글 존재 ---
@requires_login
def test_toggles_present(setting):
    assert setting.toggles.count() > 0


# --- 변경 전 기본 상태: 모든 저장/취소 버튼 비활성 ---
@requires_login
def test_save_buttons_disabled_by_default(setting):
    buttons = setting.save_buttons
    count = buttons.count()
    assert count > 0, "저장 버튼을 찾지 못함"
    for i in range(count):
        expect(buttons.nth(i)).to_be_disabled()


@requires_login
def test_cancel_buttons_disabled_by_default(setting):
    buttons = setting.cancel_buttons
    count = buttons.count()
    assert count > 0, "취소 버튼을 찾지 못함"
    for i in range(count):
        expect(buttons.nth(i)).to_be_disabled()


# --- 자동화 보류 (파괴적: 설정 변경 저장 / 항목 추가·삭제) ---
@requires_login
@pytest.mark.skip(reason="설정 변경 저장 = 공유 환경 전역 설정 변경. 파괴적, 전용 환경/롤백 필요")
def test_save_setting_change():
    ...


@requires_login
@pytest.mark.skip(reason="항목 추가/삭제(추가, 삭제 대기 리스트) = 데이터 변경. 전용 데이터 필요")
def test_add_or_delete_item():
    ...
