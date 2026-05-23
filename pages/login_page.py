from __future__ import annotations

from pages.base_page import BasePage

# NOTE: Placeholder selectors. Replace with real deepcheck 2.0 locators
# once the app/markup is available.


class LoginPage(BasePage):
    path = "/login"

    def login(self, username: str, password: str) -> None:
        self.page.get_by_label("Email").fill(username)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
