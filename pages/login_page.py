from __future__ import annotations

from config.settings import Account
from pages.base_page import BasePage

# WARNING: These selectors are best-guess conventions. They could not be
# verified against the live DOM from the test environment (egress blocked).
# Verify/replace against https://dev.deepcheck.deep-medi.com once reachable,
# e.g. run:  playwright codegen https://dev.deepcheck.deep-medi.com


class LoginPage(BasePage):
    path = "/login"

    def login(self, account: Account) -> None:
        self.page.get_by_placeholder("Email").or_(
            self.page.get_by_label("Email")
        ).first.fill(account.email)
        self.page.get_by_placeholder("Password").or_(
            self.page.get_by_label("Password")
        ).first.fill(account.password)
        self.page.get_by_role("button", name="Login").or_(
            self.page.get_by_role("button", name="로그인")
        ).first.click()
