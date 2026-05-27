"""설문 결과(/survey) 테스트 — TC 시트 '설문결과'(TC_211~235) 매핑.

level-3 계정으로 실측한 DOM(scripts/inspect_survey.py)에 맞춘 비파괴 표시
검증. 검색 실행·필터링·정렬·결과 팝업·다운로드 등 데이터/상호작용 의존 TC는
사유와 함께 grouped skip으로 문서화한다.
"""
import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.survey_page import SurveyPage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)


@pytest.fixture
def survey(logged_in_page) -> SurveyPage:
    return SurveyPage(logged_in_page).open()


# --- 화면 구성 (TC_211_001) ---
@requires_login
@pytest.mark.smoke
def test_survey_loads(survey):  # TC_211_001 화면 구성
    expect(survey.heading).to_be_visible()


@requires_login
def test_survey_type_combobox_visible(survey):  # TC_217_001 설문 항목 드롭다운 표시
    expect(survey.survey_type_combobox).to_be_visible()


@requires_login
def test_agency_filter_visible(survey):  # TC_218_001 협력사 드롭다운 표시
    expect(survey.agency_combobox).to_be_visible()


@requires_login
def test_date_input_visible(survey):  # TC_211_001 화면 구성요소: 날짜 선택기
    expect(survey.date_input).to_be_visible()


@requires_login
def test_search_box_visible(survey):  # TC_211_001 화면 구성요소: 검색 입력
    expect(survey.search_box).to_be_visible()


@requires_login
def test_excel_download_button_visible(survey):  # TC_224_001 엑셀 다운로드 버튼(팝업 동작은 skip)
    expect(survey.excel_download_button).to_be_visible()


# --- 테이블 항목 표시 (TC_235_001) ---
@requires_login
@pytest.mark.parametrize("name", SurveyPage.LIST_COLUMNS)
def test_list_columns_visible(survey, name):  # TC_235_001
    expect(survey.column_header(name)).to_be_visible()


# =====================================================================
# 자동화 보류 (TC 시트 설문결과) — 사유별 그룹. 데이터/상호작용/다운로드 의존.
# =====================================================================
@requires_login
@pytest.mark.skip(reason="새로고침 데이터 갱신 = 설문 데이터 필요 (TC_211_002)")
def test_refresh_data():
    ...


@requires_login
@pytest.mark.skip(reason="날짜 이동/date picker/빈 화면 = 데이터 갱신 필요 (TC_212_001, TC_212_002, TC_212_003)")
def test_date_navigation():
    ...


@requires_login
@pytest.mark.skip(reason="표시 항목 체크박스/시행 중 설문 목록 = 설문 데이터 필요 (TC_213_001, TC_213_002)")
def test_display_items_toggle():
    ...


@requires_login
@pytest.mark.skip(reason="Summary 카드 표시/클릭/레이아웃 = 설문 응답 데이터 필요 (TC_214_001, TC_214_002, TC_214_003, TC_214_004)")
def test_summary_cards():
    ...


@requires_login
@pytest.mark.skip(reason="검색 실행/결과/안내 = 응답 데이터 필요 (TC_215_001, TC_215_002, TC_215_003, TC_216_001, TC_216_002, TC_216_003)")
def test_search_execution():
    ...


@requires_login
@pytest.mark.skip(reason="응답여부/정렬/초기화/유형/필터 유지 = 데이터 필요 (TC_219_001, TC_219_002, TC_220_001, TC_221_001, TC_222_001, TC_223_001)")
def test_filtering_and_sort():
    ...


@requires_login
@pytest.mark.skip(reason="엑셀 다운로드 기간/파일명/다중항목 = 데이터+다운로드 핸들링 필요 (TC_224_002, TC_224_003, TC_224_004)")
def test_excel_download():
    ...


@requires_login
@pytest.mark.skip(reason="결과 팝업(행클릭/탭삭제/뱃지/항목강조/날짜변경/빈데이터) = 응답 데이터 필요 (TC_225_001, TC_226_001, TC_227_001, TC_228_001, TC_229_001, TC_229_002, TC_229_003, TC_230_001, TC_231_001)")
def test_result_popup():
    ...


@requires_login
@pytest.mark.skip(reason="결과 팝업 PDF/엑셀 다운로드 = 데이터+다운로드 핸들링 필요 (TC_232_001, TC_233_001)")
def test_result_download():
    ...


@requires_login
@pytest.mark.skip(reason="설문 답변 카드 레이아웃/증상 강조 = 응답 데이터 필요 (TC_234_001, TC_234_002)")
def test_answer_cards():
    ...


@requires_login
@pytest.mark.skip(reason="테이블 total 기술인 수 표시 = 응답 데이터 필요 (TC_235_002)")
def test_table_total():
    ...
