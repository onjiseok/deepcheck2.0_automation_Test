"""미측정 현황(/measure) 테스트 — TC 시트 '측정현황'(TC_186~210) 매핑.

level-3 계정으로 실측한 DOM(scripts/inspect_measure.py)에 맞춘 비파괴
표시/기본상태 검증. 카드 클릭 필터링·검색 실행·날짜 이동·알림 발송·엑셀·
출근자 등록 등 상호작용/발송/데이터 의존 TC는 사유와 함께 skip으로 문서화한다.
권한별(레벨2/4) TC는 권한 테스트 단계에서 별도 구현한다.
"""
import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.measure_page import MeasurePage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)


@pytest.fixture
def measure(logged_in_page) -> MeasurePage:
    return MeasurePage(logged_in_page).open()


# --- 화면 구성 (TC_186_001) ---
@requires_login
@pytest.mark.smoke
def test_measure_loads(measure):  # TC_186_001 화면 구성 요소 표시
    expect(measure.heading).to_be_visible()


# --- Summary 카드 디폴트 (TC_187_001) ---
@requires_login
def test_summary_cards_visible(measure):  # TC_187_001 전체출근인원 카드 디폴트
    expect(measure.text("전체 출근 인원")).to_be_visible()
    expect(measure.text("측정자", exact=True)).to_be_visible()
    expect(measure.text("미측정자", exact=True)).to_be_visible()


# --- 검색 필터 컨트롤 (TC_190_001~003: 전체/협력사/이름 옵션·디폴트) ---
@requires_login
def test_search_radio_default_all(measure):  # TC_190_001 디폴트 '전체'
    expect(measure.radio("전체")).to_be_checked()


@requires_login
@pytest.mark.parametrize(
    "name",
    [
        pytest.param("전체", id="TC_190_001"),
        pytest.param("협력사", id="TC_190_002"),
        pytest.param("이름", id="TC_190_003"),
    ],
)
def test_search_radio_options_visible(measure, name):
    expect(measure.radio(name)).to_be_visible()


@requires_login
def test_search_box_visible(measure):  # 검색 입력 컨트롤 표시(검색 실행은 TC_191 skip)
    expect(measure.search_box).to_be_visible()


# --- 날짜 선택 디폴트/경계 (TC_192_001 / TC_192_003) ---
@requires_login
def test_date_input_visible(measure):  # TC_192_001 날짜 디폴트 '오늘'
    expect(measure.date_input).to_be_visible()


@requires_login
def test_next_date_disabled(measure):  # TC_192_003 다음 날짜(미래) 경계 → 비활성
    expect(measure.next_date_button.last).to_be_disabled()


# --- 협력사 필터 컨트롤 (필터링 동작은 TC_193 skip) ---
@requires_login
def test_agency_filter_visible(measure):
    expect(measure.agency_combobox).to_be_visible()
    expect(measure.button("필터")).to_be_visible()


# --- 총 인원 표시 (TC_186_001 구성요소) ---
@requires_login
def test_total_count_visible(measure):
    expect(measure.total_count.first).to_be_visible()


# --- 액션 버튼 디폴트 상태 (발송/다운로드 동작은 각각 TC_194/196 skip) ---
@requires_login
def test_send_notification_disabled_by_default(measure):
    expect(measure.button("측정안내 알림 발송")).to_be_disabled()


@requires_login
def test_excel_download_disabled_by_default(measure):
    expect(measure.button("엑셀 다운로드")).to_be_disabled()


@requires_login
def test_attendee_list_button_visible(measure):  # TC_197_001 출근자 명단 버튼(팝업 동작은 skip)
    expect(measure.button("출근자 명단")).to_be_enabled()


# --- 목록 컬럼 헤더 (TC_210_001 리스트 항목 표시) ---
@requires_login
@pytest.mark.parametrize("name", MeasurePage.LIST_COLUMNS)
def test_list_columns_visible(measure, name):  # TC_210_001
    expect(measure.column_header(name)).to_be_visible()


# =====================================================================
# 자동화 보류 (TC 시트 측정현황) — 사유별 그룹. 데이터/권한/발송 의존.
# =====================================================================
@requires_login
@pytest.mark.skip(reason="Summary 카드 클릭→필터링 = 실측정 데이터 필요 (TC_188_001, TC_189_001, TC_189_002)")
def test_summary_card_click_filtering():
    ...


@requires_login
@pytest.mark.skip(reason="검색 실행/결과 = 등록된 기술인 데이터 필요 (TC_190_004, TC_191_001, TC_191_002, TC_191_003)")
def test_search_execution():
    ...


@requires_login
@pytest.mark.skip(reason="날짜 이동/date picker = 데이터 갱신 필요 (TC_192_002, TC_192_004, TC_192_005, TC_192_006, TC_192_007)")
def test_date_navigation():
    ...


@requires_login
@pytest.mark.skip(reason="협력사/현장 필터링 동작 = 데이터+권한(레벨2/4) 필요 (TC_193_001, TC_193_002, TC_193_003, TC_193_004)")
def test_agency_filtering():
    ...


@requires_login
@pytest.mark.skip(reason="측정안내 알림 발송 = 실제 알림/SMS 발송. 파괴적, 전용 데이터 필요 (TC_194_001, TC_194_002, TC_194_003, TC_194_004, TC_194_005, TC_194_006, TC_194_007, TC_194_008, TC_195_001)")
def test_send_measurement_notification():
    ...


@requires_login
@pytest.mark.skip(reason="엑셀 다운로드 = 데이터 의존 + 다운로드 핸들링 필요 (TC_196_001, TC_196_002, TC_196_003, TC_196_004, TC_196_005)")
def test_excel_download():
    ...


@requires_login
@pytest.mark.skip(reason="출근자 명단 팝업/매일 초기화/탭전환 경고 = 데이터+상호작용 (TC_197_002, TC_198_001, TC_198_002, TC_199_001)")
def test_attendee_list_dialog():
    ...


@requires_login
@pytest.mark.skip(reason="출근자 등록(파일/직접입력/오류검증) = 실제 등록/SMS. 전용 데이터 필요 (TC_200_001, TC_200_002, TC_200_003, TC_200_004, TC_200_005, TC_200_006, TC_200_007, TC_200_008, TC_201_001, TC_201_002, TC_201_003, TC_201_004, TC_201_005, TC_201_006, TC_202_001, TC_203_001, TC_203_002, TC_204_001, TC_205_001, TC_206_001)")
def test_attendee_registration():
    ...


@requires_login
@pytest.mark.skip(reason="통합 필터링/정렬 = 실측정 데이터 필요 (TC_207_001, TC_208_001, TC_208_002, TC_209_001, TC_209_002, TC_209_003, TC_210_002)")
def test_integrated_filtering_and_sort():
    ...


@requires_login
@pytest.mark.skip(reason="새로고침 데이터 갱신/레벨2·4 화면·버튼 숨김 = 데이터+권한 필요 (TC_186_002, TC_186_003, TC_197_003)")
def test_refresh_and_level_view():
    ...
