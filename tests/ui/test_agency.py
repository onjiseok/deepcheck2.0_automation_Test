"""소속업체 관리(/agency) 테스트 — TC 시트 '소속업체 관리'(TC_236~283) 매핑.

level-3 계정으로 실측한 DOM(scripts/inspect_agency.py)에 맞춘 비파괴 표시/
기본상태 검증. 협력사 추가/수정/삭제, 활성화 토글, 승인 대기 처리, 레벨2/4
권한 동작은 데이터 변경·권한·파괴적이라 grouped skip으로 문서화한다.
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


# --- 레벨3 진입 / 화면 구성 (TC_237_001) ---
@requires_login
@pytest.mark.smoke
def test_agency_loads(agency):  # TC_237_001 레벨3 모든 기능 사용(진입/화면 구성)
    expect(agency.heading).to_be_visible()


@requires_login
def test_sort_combobox_visible(agency):  # TC_267_001 이름순 정렬 컨트롤(동작은 데이터 필요)
    expect(agency.sort_combobox).to_be_visible()


@requires_login
def test_search_box_visible(agency):  # TC_266_001 협력사명 검색 컨트롤(필터 동작은 데이터 필요)
    expect(agency.search_box).to_be_visible()


@requires_login
def test_approval_pending_disabled_by_default(agency):  # 승인 대기 없음 → 버튼 비활성(처리는 TC_269~274 skip)
    expect(agency.approval_pending_button).to_be_disabled()


# --- 협력사 추가 모달 (TC_244_001 / TC_251_001) ---
@requires_login
def test_add_agency_button_enabled(agency):  # TC_244_001 [+협력사 추가] 버튼
    expect(agency.add_agency_button).to_be_enabled()


@requires_login
def test_add_dialog_opens_with_name_field(agency):  # TC_244_001 모달 표시
    agency.open_add_dialog()
    expect(agency.agency_name_field).to_be_visible()


@requires_login
def test_add_dialog_register_disabled_when_empty(agency):  # TC_251_001 협력사 선택 필수값
    agency.open_add_dialog()
    expect(agency.register_button).to_be_disabled()


# =====================================================================
# 자동화 보류 (TC 시트 소속업체 관리) — 사유별 그룹.
# =====================================================================
@requires_login
@pytest.mark.skip(reason="접근 권한(레벨2/4) = 해당 권한 계정 필요, 권한 테스트에서 구현 (TC_236_001, TC_236_002, TC_236_003, TC_238_001)")
def test_access_by_level():
    ...


@requires_login
@pytest.mark.skip(reason="즐겨찾기 아이콘/컬러/on-off = 상호작용+계정상태 (TC_239_001, TC_240_001, TC_241_001)")
def test_favorite_toggle():
    ...


@requires_login
@pytest.mark.skip(reason="사업자등록번호 표시/레벨4 미표시 = 데이터+권한 필요 (TC_242_001, TC_242_002, TC_243_001)")
def test_business_number_display():
    ...


@requires_login
@pytest.mark.skip(reason="협력사 추가 모달 상세(현장명 자동입력/드롭다운/확인팝업/실제 추가) = 데이터 생성, 파괴적 (TC_245_001, TC_246_001, TC_247_001, TC_248_001, TC_249_001, TC_250_001, TC_252_001, TC_253_001, TC_254_001)")
def test_add_agency_modal_detail():
    ...


@requires_login
@pytest.mark.skip(reason="협력사 수정 = 실제 데이터 변경, 파괴적 (TC_255_001, TC_256_001, TC_257_001, TC_258_001, TC_259_001)")
def test_edit_agency():
    ...


@requires_login
@pytest.mark.skip(reason="활성화 토글 = 측정/알림에 영향, 파괴적 (TC_260_001, TC_260_002)")
def test_activation_toggle():
    ...


@requires_login
@pytest.mark.skip(reason="협력사 삭제(개별/일괄) = 데이터 삭제, 파괴적 (TC_261_001, TC_262_001, TC_263_001, TC_264_001)")
def test_delete_agency():
    ...


@requires_login
@pytest.mark.skip(reason="현장 드롭다운 필터링 = 데이터 필요 (TC_265_001)")
def test_site_dropdown_filter():
    ...


@requires_login
@pytest.mark.skip(reason="활성화여부 필터링 = 데이터 필요 (TC_268_001, TC_268_002, TC_268_003)")
def test_activation_filter():
    ...


@requires_login
@pytest.mark.skip(reason="승인 대기 표시/처리(승인/거절/전체 승인) = 대기 데이터+파괴적 (TC_269_001, TC_270_001, TC_271_001, TC_272_001, TC_273_001, TC_274_001)")
def test_approval_pending():
    ...


@requires_login
@pytest.mark.skip(reason="레벨4 거절됨 상태/재승인/삭제 = 레벨4 권한+데이터 (TC_275_001, TC_276_001, TC_277_001, TC_278_001, TC_279_001, TC_280_001)")
def test_level4_rejected():
    ...


@requires_login
@pytest.mark.skip(reason="레벨4 현장 추가 요청 = 레벨4 권한+데이터 생성 (TC_281_001, TC_282_001)")
def test_level4_site_add():
    ...


@requires_login
@pytest.mark.skip(reason="페이지네이션 = 다량 데이터 필요 (TC_283_001, TC_283_002)")
def test_pagination():
    ...
