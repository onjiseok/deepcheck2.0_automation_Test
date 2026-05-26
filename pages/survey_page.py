from __future__ import annotations

from playwright.sync_api import Locator

from pages.base_page import BasePage

# Locators confirmed against the live level-3 설문 결과(/survey) page
# (see scripts/inspect_survey.py output). Read-only display checks.


class SurveyPage(BasePage):
    path = "/survey"

    LIST_COLUMNS = (
        "No",
        "응답여부",
        "이름",
        "협력사",
        "연락처",
        "기술인 유형",
        "설문 응답 시간",
    )

    def open(self) -> "SurveyPage":
        self.goto_via_nav("설문 결과", self.heading)
        return self

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name="설문 결과")

    def text(self, value: str, *, exact: bool = False) -> Locator:
        return self.page.get_by_text(value, exact=exact)

    def column_header(self, name: str) -> Locator:
        return self.page.get_by_role("columnheader", name=name, exact=True)

    @property
    def survey_type_combobox(self) -> Locator:
        # The label text also appears in a header; target the combobox itself.
        return self.page.get_by_role("combobox").filter(has_text="데일리 한랭질환")

    @property
    def agency_combobox(self) -> Locator:
        return self.page.get_by_text("협력사 선택")

    @property
    def date_input(self) -> Locator:
        return self.page.get_by_placeholder("YYYY.MM.DD")

    @property
    def search_box(self) -> Locator:
        return self.page.get_by_role("textbox", name="검색어를 입력하세요.")

    @property
    def excel_download_button(self) -> Locator:
        return self.page.get_by_role("button", name="엑셀 다운로드")
