"""미측정 현황(/measure) 테스트.

level-3 계정으로 실측한 DOM(scripts/inspect_measure.py)에 맞춘 비파괴
표시/기본상태 검증. 측정안내 알림 발송(=SMS/알림 발송)과 엑셀 다운로드는
파괴적/데이터 의존이라 skip한다.
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


# --- 진입 ---
@requires_login
@pytest.mark.smoke
def test_measure_loads(measure):
    expect(measure.heading).to_be_visible()


# --- 측정 현황 요약 카드 ---
@requires_login
def test_summary_cards_visible(measure):
    expect(measure.text("전체 출근 인원")).to_be_visible()
    expect(measure.text("측정자", exact=True)).to_be_visible()
    expect(measure.text("미측정자", exact=True)).to_be_visible()


# --- 검색 라디오: 디폴트 '전체' 선택 + 옵션 표시 ---
@requires_login
def test_search_radio_default_all(measure):
    expect(measure.radio("전체")).to_be_checked()


@requires_login
@pytest.mark.parametrize("name", MeasurePage.SEARCH_RADIOS)
def test_search_radio_options_visible(measure, name):
    expect(measure.radio(name)).to_be_visible()


@requires_login
def test_search_box_visible(measure):
    expect(measure.search_box).to_be_visible()


# --- 날짜 네비게이션: 다음 날짜(미래)는 비활성 ---
@requires_login
def test_date_input_visible(measure):
    expect(measure.date_input).to_be_visible()


@requires_login
def test_next_date_disabled(measure):
    expect(measure.next_date_button.last).to_be_disabled()


# --- 협력사 필터 ---
@requires_login
def test_agency_filter_visible(measure):
    expect(measure.agency_combobox).to_be_visible()
    expect(measure.button("필터")).to_be_visible()


# --- 총 인원 표시 ---
@requires_login
def test_total_count_visible(measure):
    expect(measure.total_count.first).to_be_visible()


# --- 액션 버튼 디폴트 상태 (선택 없음 → 발송/다운로드 비활성) ---
@requires_login
def test_send_notification_disabled_by_default(measure):
    expect(measure.button("측정안내 알림 발송")).to_be_disabled()


@requires_login
def test_excel_download_disabled_by_default(measure):
    expect(measure.button("엑셀 다운로드")).to_be_disabled()


@requires_login
def test_attendee_list_button_visible(measure):
    expect(measure.button("출근자 명단")).to_be_enabled()


# --- 목록 컬럼 헤더 ---
@requires_login
@pytest.mark.parametrize("name", MeasurePage.LIST_COLUMNS)
def test_list_columns_visible(measure, name):
    expect(measure.column_header(name)).to_be_visible()


# --- 자동화 보류 ---
@requires_login
@pytest.mark.skip(reason="측정안내 알림 발송 = 실제 알림/SMS 발송. 대상 선택 필요 + 파괴적, 전용 데이터 필요")
def test_send_measurement_notification():
    ...


@requires_login
@pytest.mark.skip(reason="엑셀 다운로드 검증 = 데이터 의존 + 다운로드 핸들링 별도 구현 필요")
def test_excel_download():
    ...
