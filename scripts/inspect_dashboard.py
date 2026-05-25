"""Diagnostic helper: log in (level 3) and dump the dashboard's visible text +
a screenshot, so card titles and landmarks can be confirmed for test coverage.

Run (with .env configured, browser visible):
    python scripts/inspect_dashboard.py

Outputs artifacts/dashboard.png and prints the page text. Throwaway aid.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from playwright.sync_api import sync_playwright

from config.settings import settings

OUT = pathlib.Path("artifacts")
OUT.mkdir(exist_ok=True)
LOGIN_URL = settings.base_url.rstrip("/") + "/login"


def main():
    acc = settings.account(3)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_context().new_page()
        page.goto(LOGIN_URL)
        page.get_by_role("textbox", name="이메일").fill(acc.email)
        page.get_by_role("textbox", name="비밀번호").fill(acc.password)
        page.get_by_role("button", name="로그인").click()
        page.wait_for_url(re.compile(r"/dashboard"), timeout=20000)
        page.wait_for_timeout(3000)
        page.screenshot(path=str(OUT / "dashboard.png"), full_page=True)
        print(f"\n===== dashboard | url={page.url} =====")
        print(page.locator("body").inner_text())
        browser.close()
    print(f"\nScreenshot saved: {(OUT / 'dashboard.png').resolve()}")


if __name__ == "__main__":
    main()
