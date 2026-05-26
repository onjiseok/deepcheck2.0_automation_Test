from __future__ import annotations

from playwright.sync_api import Locator

from pages.base_page import BasePage

# Locators confirmed against the live level-3 소속업체 관리(/agency) page and the
# 협력사 추가 dialog (see scripts/inspect_agency.py output). Read-only: never
# submits 등록, so no agency is created.


class AgencyPage(BasePage):
    path = "/agency"

    def open(self) -> "AgencyPage":
        self.goto_via_nav("소속업체 관리", self.heading)
        return self

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name="소속업체 관리")

    def text(self, value: str, *, exact: bool = False) -> Locator:
        return self.page.get_by_text(value, exact=exact)

    @property
    def sort_combobox(self) -> Locator:
        return self.page.get_by_text("이름 순")

    @property
    def search_box(self) -> Locator:
        return self.page.get_by_role("textbox", name="협력사명을 입력해 주세요.")

    @property
    def approval_pending_button(self) -> Locator:
        return self.page.get_by_role("button", name="승인 대기")

    @property
    def add_agency_button(self) -> Locator:
        return self.page.get_by_role("button", name="협력사 추가")

    # --- 협력사 추가 다이얼로그 ---
    @property
    def dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    @property
    def agency_name_field(self) -> Locator:
        return self.dialog.get_by_placeholder("추가할 협력사명을 입력해 주십시오.")

    @property
    def register_button(self) -> Locator:
        return self.dialog.get_by_role("button", name="등록", exact=True)

    def open_add_dialog(self) -> "AgencyPage":
        self.add_agency_button.click()
        self.dialog.wait_for(state="visible", timeout=10000)
        return self
