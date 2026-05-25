"""Diagnostic helper: capture the real inline-validation message the login
screen shows for each password input, so test assertions use exact wording.

Run (with .env configured, browser visible):
    python scripts/inspect_login.py

Prints 'PW=<input>  ERROR=<message>' for each case. Throwaway aid, not a test.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from playwright.sync_api import sync_playwright

from config.settings import settings

LOGIN_URL = settings.base_url.rstrip("/") + "/login"

# Static labels on the login screen; anything else is the validation message.
KNOWN = {"이메일", "비밀번호", "로그인", "비밀번호 재설정", "협력사 등록하기"}

PASSWORD_INPUTS = ["", "abcdefgh", "Qw1!abc", "aaaa1234!", "abcd1234!", "test1234!"]


def error_text(page) -> str:
    lines = [ln.strip() for ln in page.locator("body").inner_text().splitlines()]
    extras = [ln for ln in lines if ln and ln not in KNOWN]
    return " | ".join(extras) if extras else "(no message)"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)

        print("\n--- password validation messages (login screen) ---")
        for value in PASSWORD_INPUTS:
            page = browser.new_context().new_page()
            page.goto(LOGIN_URL)
            if value:
                page.get_by_role("textbox", name="비밀번호").fill(value)
            page.locator("body").click()
            page.wait_for_timeout(800)
            print(f"PW={value!r:14}  ERROR={error_text(page)}")
            page.close()

        browser.close()


if __name__ == "__main__":
    main()
