"""Login screen tests, derived from TC sheet 'Deep check 2.0(웹) v1.0.0'.

Each test/parameter id carries its TC_ID for traceability in Grafana.
Selectors beyond the email/password fields are inferred from the spec and
should be confirmed by a verification run against the dev site.
"""
import re

import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui]

requires_app = pytest.mark.skipif(not settings.base_url, reason="BASE_URL not configured")


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


# --- 이메일 입력 유효성 (focus-out 안내문구) ---
EMAIL_VALIDATION = [
    ("TC_002_001", "", "이메일을 입력해 주세요."),
    ("TC_003_001", "a", "2글자 이상 입력해 주세요."),
    ("TC_004_001", "testuser", "올바른 이메일 형식을 입력해 주세요."),
    ("TC_001_006", "test@", "올바른 이메일 형식을 입력해 주세요."),
]


@requires_app
@pytest.mark.parametrize("tc_id,value,message", EMAIL_VALIDATION, ids=[c[0] for c in EMAIL_VALIDATION])
def test_email_validation_message(login_page, tc_id, value, message):
    login_page.fill_email(value)
    login_page.blur()
    expect(login_page.message(message)).to_be_visible()


# --- 비밀번호 입력 유효성 (focus-out 안내문구) ---
PASSWORD_VALIDATION = [
    ("TC_010_001", "", "비밀번호를 입력해 주세요."),
    ("TC_011_001", "abcdefgh", "영문,숫자,특수문자를 포함하여 8글자 이상 입력해 주십시오."),
    ("TC_012_001", "Qw1!abc", "영문,숫자,특수문자를 포함하여 8글자 이상 입력해 주십시오."),
    ("TC_013_001", "aaaa1234!", "보안을 위해 동일한 문자는 4자리 이상 사용할 수 없습니다."),
    ("TC_014_001", "abcd1234!", "보안을 위해 연속된 문자는 4자리 이상 사용할 수 없습니다."),
    ("TC_015_001", "test1234!", "보안을 위해 연속된 문자는 4자리 이상 사용할 수 없습니다."),
]


@requires_app
@pytest.mark.parametrize("tc_id,value,message", PASSWORD_VALIDATION, ids=[c[0] for c in PASSWORD_VALIDATION])
def test_password_validation_message(login_page, tc_id, value, message):
    login_page.fill_password(value)
    login_page.blur()
    expect(login_page.message(message)).to_be_visible()


# --- 로그인 버튼 활성화/비활성화 ---
@requires_app
def test_login_button_disabled_when_email_empty(login_page):  # TC_001_001 / TC_022_002
    login_page.fill_password("qwer1234!")
    assert login_page.login_button.is_disabled()


@requires_app
def test_login_button_disabled_when_password_empty(login_page):  # TC_009_001
    login_page.fill_email("test@deep.com")
    assert login_page.login_button.is_disabled()


@requires_app
def test_login_button_enabled_when_both_valid(login_page):  # TC_022_001
    login_page.fill_email("test@deep.com")
    login_page.fill_password("qwer1234!")
    assert login_page.login_button.is_enabled()


@requires_app
def test_login_button_disabled_on_error_state(login_page):  # TC_022_003
    login_page.fill_email("a")
    login_page.fill_password("qwer1234!")
    login_page.blur()
    assert login_page.login_button.is_disabled()


# --- 비밀번호 마스킹 (TC_009_002) ---
@requires_app
def test_password_masked_by_default(login_page):
    assert login_page.password.get_attribute("type") == "password"


# --- 로그인 성공/실패 ---
@requires_app
@pytest.mark.smoke
@pytest.mark.skipif(3 not in settings.accounts, reason="level-3 account not configured")
def test_login_success(page, account):  # TC_024_001
    LoginPage(page).open().login(account(3))
    expect(page).not_to_have_url(re.compile(r"/login"))


@requires_app
def test_login_fail_wrong_password(login_page):  # TC_023_002
    login_page.fill_email("careup_test@deep-medi.com")
    login_page.fill_password("wrongpw1!")
    login_page.submit()
    # Spacing of the message varies in the spec; match the distinctive phrasing.
    expect(login_page.page.get_by_text(re.compile("이메일.*비밀번호.*확인"))).to_be_visible()


# --- 자동화 보류: 별도 결정/인프라 필요 (아래 사유 참조) ---
@requires_app
@pytest.mark.skip(reason="계정 잠금: 공유 dev 계정을 잠그게 되어 위험. 전용 계정/DB 리셋 필요 (TC_023_003/004)")
def test_account_lock_after_5_failures():
    ...


@requires_app
@pytest.mark.skip(reason="메일 수신 검증 필요(Mailosaur 등 테스트 메일박스). 인프라 미정 (TC_026_001/002)")
def test_password_reset_email_received():
    ...


@requires_app
@pytest.mark.skip(reason="실제 비밀번호 변경 = 공유 계정 파괴적. 전용 계정 필요 (TC_027_005/007)")
def test_password_reset_changes_password():
    ...
