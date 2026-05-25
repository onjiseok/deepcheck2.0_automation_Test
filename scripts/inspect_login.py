"""Diagnostic helper: capture what the real login screen does for the cases
that failed verification, so selectors/messages can be confirmed.

Run (with .env configured, browser visible):
    python scripts/inspect_login.py

Outputs screenshots to ./artifacts/ and prints any visible page text.
This is a throwaway investigation aid, not part of the test suite.
"""
import pathlib

from playwright.sync_api import sync_playwright

from config.settings import settings

OUT = pathlib.Path("artifacts")
OUT.mkdir(exist_ok=True)
LOGIN_URL = settings.base_url.rstrip("/") + "/login"


def dump(page, name):
    page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)
    text = page.locator("body").inner_text()
    print(f"\n===== {name} | url={page.url} =====")
    print(text[:1500])


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)

        # A) password complexity message on the LOGIN screen?
        page = browser.new_context().new_page()
        page.goto(LOGIN_URL)
        page.get_by_role("textbox", name="비밀번호").fill("abcdefgh")
        page.locator("body").click()
        page.wait_for_timeout(1500)
        dump(page, "pw_complexity_abcdefgh")

        # B) wrong-password login failure popup
        page = browser.new_context().new_page()
        page.goto(LOGIN_URL)
        page.get_by_role("textbox", name="이메일").fill("careup_test@deep-medi.com")
        page.get_by_role("textbox", name="비밀번호").fill("wrongpw1!")
        page.get_by_role("button", name="로그인").click()
        page.wait_for_timeout(3000)
        dump(page, "login_fail")

        # C) successful login destination
        page = browser.new_context().new_page()
        page.goto(LOGIN_URL)
        acc = settings.account(3)
        page.get_by_role("textbox", name="이메일").fill(acc.email)
        page.get_by_role("textbox", name="비밀번호").fill(acc.password)
        page.get_by_role("button", name="로그인").click()
        page.wait_for_timeout(4000)
        dump(page, "login_success")

        browser.close()
    print(f"\nScreenshots saved in: {OUT.resolve()}")


if __name__ == "__main__":
    main()
