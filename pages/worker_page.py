from __future__ import annotations

import re

from playwright.sync_api import Locator

from pages.base_page import BasePage

# Locators confirmed against the live level-3 기술인 관리 page and the
# 사전가입자 등록 dialog (see scripts/inspect_worker.py output).
#
# SAFETY: the 직접 입력 grid's first editable row is row 2. Submitting via
# [오류 확인 및 등록] only creates records for rows with NO validation error;
# any row containing an error is reported in the error table and is NOT
# registered (so no SMS is sent). Tests here therefore always submit rows that
# are guaranteed to fail validation (e.g. a too-short phone number).


class WorkerPage(BasePage):
    path = "/worker"

    FIELD_LABELS = (
        "전화번호",
        "이름",
        "측정앱 사용",
        "협력사",
        "보정값(수축기)",
        "보정값(이완기)",
    )

    def open(self) -> "WorkerPage":
        # SPA client-side nav (pushState) fires no 'load' event, so wait on a
        # worker-page-only element instead of wait_for_url(... until='load').
        self.page.get_by_role("link", name="기술인 관리").click()
        self.register_button.wait_for(state="visible", timeout=20000)
        return self

    # --- 사전가입자 등록 진입 ---
    @property
    def register_button(self) -> Locator:
        return self.page.get_by_role("button", name="사전가입자 등록")

    @property
    def dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    def tab(self, name_pattern: str) -> Locator:
        return self.page.get_by_role("tab", name=re.compile(name_pattern))

    def open_registration(self, *, direct_input: bool = True) -> "WorkerPage":
        self.register_button.click()
        self.dialog.wait_for(state="visible", timeout=10000)
        if direct_input:
            self.tab("직접 입력").click()
        return self

    # --- 직접 입력 그리드 (행 번호는 2부터 시작) ---
    def field(self, label: str, row: int = 2) -> Locator:
        return self.page.get_by_role("textbox", name=f"{label} {row}행")

    def phone(self, row: int = 2) -> Locator:
        return self.field("전화번호", row)

    def name(self, row: int = 2) -> Locator:
        return self.field("이름", row)

    def agency(self, row: int = 2) -> Locator:
        return self.field("협력사", row)

    @property
    def submit_button(self) -> Locator:
        return self.dialog.get_by_role("button", name="오류 확인 및 등록", exact=True)

    def fill_row(
        self,
        row: int = 2,
        *,
        phone: str | None = None,
        name: str | None = None,
        agency: str | None = None,
    ) -> None:
        if phone is not None:
            self.phone(row).fill(phone)
        if name is not None:
            self.name(row).fill(name)
        if agency is not None:
            self.agency(row).fill(agency)

    def submit(self) -> None:
        self.submit_button.click()

    # --- 제출 결과 ---
    @property
    def result_alert(self) -> Locator:
        return self.dialog.get_by_role("alert")

    def result_summary(self) -> Locator:
        return self.dialog.get_by_text(re.compile(r"등록되지 않은 기술인"))

    def error_cell(self, text: str) -> Locator:
        return self.dialog.get_by_role("cell", name=text, exact=True)
