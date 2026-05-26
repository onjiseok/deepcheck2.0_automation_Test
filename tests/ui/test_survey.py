"""설문 결과(/survey) 테스트.

level-3 계정으로 실측한 DOM(scripts/inspect_survey.py)에 맞춘 비파괴
표시 검증. 엑셀 다운로드는 데이터 의존 + 다운로드 핸들링이 필요해 skip한다.
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


@requires_login
@pytest.mark.smoke
def test_survey_loads(survey):
    expect(survey.heading).to_be_visible()


@requires_login
def test_survey_type_combobox_visible(survey):
    expect(survey.survey_type_combobox).to_be_visible()


@requires_login
def test_agency_filter_visible(survey):
    expect(survey.agency_combobox).to_be_visible()


@requires_login
def test_date_input_visible(survey):
    expect(survey.date_input).to_be_visible()


@requires_login
def test_search_box_visible(survey):
    expect(survey.search_box).to_be_visible()


@requires_login
def test_excel_download_button_visible(survey):
    expect(survey.excel_download_button).to_be_visible()


@requires_login
@pytest.mark.parametrize("name", SurveyPage.LIST_COLUMNS)
def test_list_columns_visible(survey, name):
    expect(survey.column_header(name)).to_be_visible()


# --- 자동화 보류 ---
@requires_login
@pytest.mark.skip(reason="엑셀 다운로드 검증 = 데이터 의존 + 다운로드 핸들링 별도 구현 필요")
def test_excel_download():
    ...
