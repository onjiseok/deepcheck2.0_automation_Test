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
    pytest.param("", "비밀번호를 입력해 주세요.", id="TC_010_001"),
    pytest.param("abcdefgh", "영문, 숫자, 특수문자가 포함되어야 합니다.", id="TC_011_001"),
    pytest.param("Qw1!abc", "영문, 숫자, 특수문자가 포함되어야 합니다.", id="TC_012_001"),
]


@requires_app
@pytest.mark.parametrize("value,message", PASSWORD_VALIDATION)
def test_password_validation_message(login_page, value, message):
    login_page.fill_password(value)
    login_page.blur()
    expect(login_page.message(message)).to_be_visible()


# 로그인 화면은 "영문/숫자/특수문자 포함" 규칙만 검증하고, 동일/연속문자 4연속
# 규칙은 검증하지 않음(실측). 형식을 만족하는 비밀번호는 에러가 표시되지 않는다.
# (동일/연속문자 규칙은 비밀번호 재설정 화면 TC_026_007~009에서 검증)
PASSWORD_NO_ERROR = [
    pytest.param("aaaa1234!", id="TC_013_001"),
    pytest.param("abcd1234!", id="TC_014_001"),
    pytest.param("test1234!", id="TC_015_001"),
]


@requires_app
@pytest.mark.parametrize("value", PASSWORD_NO_ERROR)
def test_password_format_valid_shows_no_error(login_page, value):
    login_page.fill_password(value)
    login_page.blur()
    expect(login_page.message("영문, 숫자, 특수문자가 포함되어야 합니다.")).not_to_be_visible()


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
    # The failure surfaces in a popup; allow for auth round-trip latency.
    expect(login_page.login_fail_dialog).to_contain_text(
        "이메일 또는 비밀번호를 다시 한번 확인", timeout=15000
    )


# --- Placeholder / 비밀번호 보기 토글 / 경계값 (추가 표시 검증) ---
@requires_app
def test_email_placeholder(login_page):  # TC_001_011
    expect(login_page.page.get_by_placeholder("이메일 주소를 입력해 주세요.")).to_be_visible()


@requires_app
def test_password_placeholder(login_page):  # TC_009_006
    expect(login_page.page.get_by_placeholder("비밀번호를 입력해 주세요.")).to_be_visible()


@requires_app
def test_password_visibility_toggle(login_page):  # TC_009_003, TC_009_004
    login_page.fill_password("qwer1234!")
    expect(login_page.password).to_have_attribute("type", "password")
    login_page.password_visibility_toggle.click()
    expect(login_page.password).to_have_attribute("type", "text")
    login_page.password_visibility_toggle.click()
    expect(login_page.password).to_have_attribute("type", "password")


@requires_app
def test_email_2char_no_length_error(login_page):  # TC_001_003, TC_006_001 (경계값 2글자)
    login_page.fill_email("ab")
    login_page.blur()
    expect(login_page.message("2글자 이상 입력해 주세요.")).not_to_be_visible()


# --- 자동화 보류: 입력 제한/경계값(동작 미확정) ---
@requires_app
@pytest.mark.skip(reason="이메일 입력 제한/경계/자동변환 = 필드단계 제한 동작 미확정(실측 필요), 일부 미적용 가능 (TC_001_002, TC_001_004, TC_001_005, TC_001_007, TC_001_008, TC_001_009, TC_001_010, TC_005_001, TC_007_001, TC_008_001)")
def test_email_input_restriction_and_boundary():
    ...


@requires_app
@pytest.mark.skip(reason="비밀번호 입력 제한/전체삭제/경계 = 필드단계 제한 동작 미확정(실측 필요) (TC_009_005, TC_009_007, TC_016_001, TC_017_001, TC_018_001, TC_019_001, TC_020_001, TC_021_001)")
def test_password_input_restriction_and_boundary():
    ...


@requires_app
@pytest.mark.skip(reason="입력값 수정으로 error 해소 후 로그인 버튼 재비활성 = 동작 시퀀스, 추후 자동화 (TC_022_004)")
def test_login_button_error_recovery():
    ...


@requires_app
@pytest.mark.skip(reason="존재하지 않는 메일/계정 잠금 해제/팝업 닫힘 = 공유 계정 잠금 위험·데이터 (TC_023_001, TC_023_004, TC_023_005)")
def test_login_failure_popup():
    ...


@requires_app
@pytest.mark.skip(reason="비밀번호 재설정 요청 페이지(LGI) = 별도 페이지 객체 + 메일 발송, 전용 메일박스 필요 (TC_025_001, TC_025_002, TC_025_003, TC_025_004, TC_025_005, TC_025_006, TC_025_007, TC_025_008, TC_025_009, TC_025_010, TC_025_011, TC_025_012, TC_025_013)")
def test_password_reset_request_page():
    ...


@requires_app
@pytest.mark.skip(reason="메일 링크 진입 후 새 비밀번호 설정 페이지 = 메일 수신(테스트 메일박스) 필요 (TC_026_002, TC_026_003, TC_026_004, TC_026_005, TC_026_006, TC_026_008, TC_026_009, TC_026_010, TC_026_011, TC_026_012, TC_026_013, TC_026_014)")
def test_password_reset_new_password_page():
    ...


@requires_app
@pytest.mark.skip(reason="비밀번호 변경 진행 = 공유 계정 비밀번호 변경, 파괴적 + 메일 필요 (TC_027_001, TC_027_002, TC_027_003, TC_027_004, TC_027_006, TC_027_007, TC_027_008)")
def test_password_change_flow():
    ...


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
