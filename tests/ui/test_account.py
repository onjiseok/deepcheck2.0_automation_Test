"""계정 관리(/account/site) 테스트 — TC 시트 '계정 관리'(TC_530~598) 매핑.

level-3 계정으로 실측한 DOM(scripts/inspect_account.py)에 맞춘 비파괴 표시/
기본상태 검증. 계정 등록/수정/삭제, 인증 메일 재발송, 알림 설정, 레벨2/4
권한 동작은 데이터 변경·메일 발송·권한 의존이라 grouped skip으로 문서화한다.
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


# --- 레벨3 진입 / 서브 탭 (TC_532_001 / TC_598_001~002) ---
@requires_login
@pytest.mark.smoke
def test_account_loads(account_page):  # TC_532_001 레벨3 진입/기능 사용
    expect(account_page.page).to_have_url(re.compile(r"/account/site"))
    expect(account_page.add_manager_button).to_be_visible()


@requires_login
@pytest.mark.parametrize(
    "name",
    [
        pytest.param("현장 관리자", id="TC_598_001"),
        pytest.param("협력사 관리자", id="TC_598_002"),
    ],
)
def test_subnav_links_visible(account_page, name):  # 탭 표시(클릭 후 리스트는 데이터 의존)
    expect(account_page.subnav_link(name)).to_be_visible()


# --- 검색 / 인증여부 필터 (TC_549_001 / TC_538_001) ---
@requires_login
def test_search_box_visible(account_page):  # TC_549_001 관리자 검색창(검색 동작은 skip)
    expect(account_page.search_box).to_be_visible()


@requires_login
def test_auth_filter_visible(account_page):  # TC_538_001 인증여부 필터 디폴트 표시
    expect(account_page.text("인증여부")).to_be_visible()


@requires_login
def test_total_count_visible(account_page):  # 화면 구성요소(총 N명)
    expect(account_page.total_count.first).to_be_visible()


# --- 액션 버튼 기본 상태 (TC_593_001 / TC_550_001) ---
@requires_login
def test_delete_disabled_by_default(account_page):  # TC_593_001 선택 없음 → 삭제 비활성
    expect(account_page.delete_button).to_be_disabled()


@requires_login
def test_add_manager_button_enabled(account_page):  # TC_550_001 현장 관리자 추가 버튼
    expect(account_page.add_manager_button).to_be_enabled()


# --- 목록 컬럼 (화면 구성요소) ---
@requires_login
@pytest.mark.parametrize("name", AccountPage.LIST_COLUMNS)
def test_list_columns_visible(account_page, name):
    expect(account_page.column_header(name)).to_be_visible()


# --- 현장관리자 추가 모달 (TC_550_001 / 필수값 TC_572·574·577) ---
@requires_login
def test_add_dialog_opens_with_fields(account_page):  # TC_550_001 모달 표시
    account_page.open_add_dialog()
    for field in AccountPage.ADD_FIELDS:
        expect(account_page.add_field(field)).to_be_visible()


@requires_login
def test_add_dialog_register_disabled_when_empty(account_page):
    # 빈 폼 → 등록 비활성: 이름/이메일/전화번호 필수값 (TC_572_001, TC_574_001, TC_577_001)
    account_page.open_add_dialog()
    expect(account_page.register_button).to_be_disabled()


# =====================================================================
# 자동화 보류 (TC 시트 계정 관리) — 사유별 그룹.
# =====================================================================
@requires_login
@pytest.mark.skip(reason="접근 권한(레벨2/4)/네비바 연동 = 해당 권한 계정 필요 (TC_530_001, TC_531_001, TC_533_001, TC_534_001, TC_535_001, TC_536_001)")
def test_access_by_level():
    ...


@requires_login
@pytest.mark.skip(reason="필터 라벨/인증여부 옵션·필터링 = 데이터 필요 (TC_537_001, TC_539_001, TC_540_001, TC_541_001, TC_542_001)")
def test_auth_filter_options():
    ...


@requires_login
@pytest.mark.skip(reason="인증 재시도 = 실제 인증 메일 재발송. 파괴적, 미인증 계정 데이터 필요 (TC_543_001, TC_544_001, TC_545_001, TC_546_001, TC_547_001, TC_548_001)")
def test_auth_retry():
    ...


@requires_login
@pytest.mark.skip(reason="검색 실행/규칙/시점 = 데이터 필요 (TC_549_002, TC_549_003)")
def test_search_execution():
    ...


@requires_login
@pytest.mark.skip(reason="추가 모달 상세(현장 디폴트/다중 현장 카드/중복 제외/정렬/삭제) = 상호작용+데이터 (TC_551_001, TC_552_001, TC_553_001, TC_554_001, TC_555_001, TC_556_001, TC_557_001, TC_558_001, TC_559_001)")
def test_add_manager_modal_detail():
    ...


@requires_login
@pytest.mark.skip(reason="알림받을 협력사 리스트/선택/높이 = 협력사 데이터 필요 (TC_560_001, TC_561_001, TC_562_001, TC_563_001, TC_564_001, TC_565_001, TC_566_001)")
def test_notify_agencies():
    ...


@requires_login
@pytest.mark.skip(reason="알림 발송 방식(위치/checkbox/디폴트/개별/일괄) = 상호작용 (TC_567_001, TC_568_001, TC_569_001, TC_570_001, TC_571_001)")
def test_notify_method():
    ...


@requires_login
@pytest.mark.skip(reason="관리자 정보 검증(직책/이메일 형식·중복/전화 형식) = 입력+서버 검증, 데이터 필요 (TC_573_001, TC_575_001, TC_576_001, TC_578_001)")
def test_manager_info_validation():
    ...


@requires_login
@pytest.mark.skip(reason="현장 관리자 정상 등록 = 실제 계정 생성 + 인증 메일 발송. 파괴적 (TC_579_001)")
def test_register_manager():
    ...


@requires_login
@pytest.mark.skip(reason="관리자 수정(진입/기존 데이터/수정) = 실제 데이터 변경, 파괴적 (TC_580_001, TC_581_001, TC_582_001)")
def test_edit_manager():
    ...


@requires_login
@pytest.mark.skip(reason="협력사 관리자 추가(드롭다운/표시방식/필수/알림/레벨4) = 데이터+권한, 파괴적 (TC_583_001, TC_584_001, TC_585_001, TC_586_001, TC_587_001, TC_588_001, TC_589_001, TC_590_001)")
def test_agency_manager_add():
    ...


@requires_login
@pytest.mark.skip(reason="협력사 관리자 수정 = 실제 데이터 변경, 파괴적 (TC_591_001, TC_592_001)")
def test_agency_manager_edit():
    ...


@requires_login
@pytest.mark.skip(reason="관리자 삭제(일괄/개별/완료/취소) = 데이터 삭제, 파괴적 (TC_594_001, TC_595_001, TC_596_001, TC_597_001)")
def test_delete_manager():
    ...
