from __future__ import annotations

import re

from playwright.sync_api import Locator

from pages.base_page import BasePage

# Locators below are confirmed against the live level-3 dashboard DOM
# (see scripts/inspect_dashboard.py output). 시스템 공지 카드는 현재 환경에
# 존재하지 않아 다루지 않는다(TC_147 - QA 확인 필요).


class DashboardPage(BasePage):
    path = "/dashboard"

    NAV_ITEMS = (
        "대시보드",
        "기술인 관리",
        "미측정 현황",
        "설문 결과",
        "소속업체 관리",
        "계정 관리",
        "설정",
    )

    def text(self, value: str, *, exact: bool = False) -> Locator:
        return self.page.get_by_text(value, exact=exact)

    def nav_link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name)

    def button(self, name: str, *, exact: bool = False) -> Locator:
        return self.page.get_by_role("button", name=name, exact=exact)

    def link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name)

    def column_header(self, name: str) -> Locator:
        return self.page.get_by_role("columnheader", name=name)

    @property
    def data_timestamp(self) -> Locator:
        return self.page.get_by_text(re.compile(r"\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}"))

    @property
    def expired_included_switch(self) -> Locator:
        return self.page.get_by_role("switch")
