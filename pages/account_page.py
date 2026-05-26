from __future__ import annotations

import re

from playwright.sync_api import Locator

from pages.base_page import BasePage

# Locators confirmed against the live level-3 계정 관리(/account/site) page and
# the 현장 관리자 추가 dialog (see scripts/inspect_account.py output).
# All checks are read-only: no account is created, deleted, or re-invited.


class AccountPage(BasePage):
    path = "/account/site"

    SUBNAV = ("현장 관리자", "협력사 관리자")
    LIST_COLUMNS = ("No", "이름", "직책", "이메일", "연락처", "알림 수신")
    # input[name=...] of the 현장 관리자 추가 dialog
    ADD_FIELDS = ("name", "position", "email", "phone")

    def open(self) -> "AccountPage":
        self.goto_via_nav("계정 관리", self.add_manager_button)
        return self

    def text(self, value: str, *, exact: bool = False) -> Locator:
        return self.page.get_by_text(value, exact=exact)

    def subnav_link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    def column_header(self, name: str) -> Locator:
        return self.page.get_by_role("columnheader", name=name, exact=True)

    @property
    def search_box(self) -> Locator:
        return self.page.get_by_role("textbox", name="이메일 또는 이름을 입력해 주세요.")

    @property
    def total_count(self) -> Locator:
        return self.page.get_by_text(re.compile(r"총\s*\d+명"))

    @property
    def delete_button(self) -> Locator:
        return self.page.get_by_role("button", name="삭제", exact=True)

    @property
    def add_manager_button(self) -> Locator:
        return self.page.get_by_role("button", name="현장 관리자 추가")

    # --- 현장 관리자 추가 다이얼로그 ---
    @property
    def dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    def add_field(self, name: str) -> Locator:
        return self.dialog.locator(f'input[name="{name}"]')

    @property
    def register_button(self) -> Locator:
        return self.dialog.get_by_role("button", name="등록", exact=True)

    def open_add_dialog(self) -> "AccountPage":
        self.add_manager_button.click()
        self.dialog.wait_for(state="visible", timeout=10000)
        return self
