from __future__ import annotations

from playwright.sync_api import Locator, Page

from config.settings import Account
from pages.base_page import BasePage

# Confirmed selectors (from Playwright codegen on the live dev site):
#   - email field    : role=textbox name="이메일"
#   - password field : role=textbox name="비밀번호"
# Other element locators (buttons, clear/visibility icons, reset link) are
# inferred from the test spec text and need a verification run to confirm.


class LoginPage(BasePage):
    path = "/login"

    # --- elements ---
    @property
    def email(self) -> Locator:
        return self.page.get_by_role("textbox", name="이메일")

    @property
    def password(self) -> Locator:
        return self.page.get_by_role("textbox", name="비밀번호")

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role("button", name="로그인")

    @property
    def reset_password_link(self) -> Locator:
        return self.page.get_by_text("비밀번호 재설정")

    @property
    def login_fail_dialog(self) -> Locator:
        """Popup shown on failed login (로그인 실패)."""
        return self.page.get_by_role("dialog")

    def message(self, text: str) -> Locator:
        """Inline validation/guidance text, matched by its exact wording."""
        return self.page.get_by_text(text)

    # --- actions ---
    def fill_email(self, value: str) -> "LoginPage":
        self.email.fill(value)
        return self

    def fill_password(self, value: str) -> "LoginPage":
        self.password.fill(value)
        return self

    def blur(self) -> None:
        self.page.locator("body").click()

    def submit(self) -> None:
        self.login_button.click()

    def login(self, account: Account) -> None:
        self.fill_email(account.email)
        self.fill_password(account.password)
        self.submit()
