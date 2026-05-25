from __future__ import annotations

import re

from playwright.sync_api import Locator

from pages.base_page import BasePage

# Locators confirmed against the live level-3 미측정 현황 page
# (see scripts/inspect_measure.py output). All read-only/display checks.


class MeasurePage(BasePage):
    path = "/measure"

    SEARCH_RADIOS = ("전체", "협력사", "이름")
    LIST_COLUMNS = (
        "No",
        "측정여부",
        "이름",
        "협력사",
        "연락처",
        "유형",
        "측정시간",
    )

    def open(self) -> "MeasurePage":
        # SPA pushState nav fires no 'load' event; wait on a measure-only element.
        self.page.get_by_role("link", name="미측정 현황").click()
        self.heading.wait_for(state="visible", timeout=20000)
        return self

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name="미측정 현황")

    def text(self, value: str, *, exact: bool = False) -> Locator:
        return self.page.get_by_text(value, exact=exact)

    def button(self, name: str, *, exact: bool = False) -> Locator:
        return self.page.get_by_role("button", name=name, exact=exact)

    def radio(self, name: str) -> Locator:
        return self.page.get_by_role("radio", name=name, exact=True)

    def column_header(self, name: str) -> Locator:
        return self.page.get_by_role("columnheader", name=name, exact=True)

    @property
    def search_box(self) -> Locator:
        return self.page.get_by_role("textbox", name="검색어를 입력하세요.")

    @property
    def date_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="날짜 입력")

    @property
    def next_date_button(self) -> Locator:
        return self.page.get_by_role("button", name="다음 날짜", exact=True)

    @property
    def agency_combobox(self) -> Locator:
        return self.page.get_by_text("협력사 선택")

    @property
    def total_count(self) -> Locator:
        return self.page.get_by_text(re.compile(r"총\s*\d+명"))
