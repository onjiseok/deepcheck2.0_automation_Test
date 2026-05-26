from __future__ import annotations

from playwright.sync_api import Locator

from pages.base_page import BasePage

# Locators confirmed against the live level-3 설정(/setting/basic) page
# (see scripts/inspect_setting.py output). Read-only: never clicks 저장, so no
# setting is changed. Each setting section has its own 취소/저장 pair, both
# disabled until a change is made.


class SettingPage(BasePage):
    path = "/setting/basic"

    SUBNAV = ("기본 설정", "설문조사", "알림 관리", "기기 관리")

    def open(self) -> "SettingPage":
        self.goto_via_nav("설정", self.subnav_link("기본 설정"))
        # Section content (toggles, 저장/취소) is lazily rendered after nav.
        self.toggles.first.wait_for(state="visible", timeout=15000)
        return self

    def subnav_link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    @property
    def save_buttons(self) -> Locator:
        return self.page.get_by_role("button", name="저장", exact=True)

    @property
    def cancel_buttons(self) -> Locator:
        return self.page.get_by_role("button", name="취소", exact=True)

    @property
    def toggles(self) -> Locator:
        return self.page.get_by_role("switch")
