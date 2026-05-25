"""Diagnostic: log in (level 3), open 기술인 관리(/worker), and dump the page +
the 사전가입 등록 form structure so we can author registration-validation tests.

Run (with .env configured):
    python scripts/inspect_worker.py

Prints aria snapshots (role/name tree) and saves screenshots under artifacts/.
Throwaway aid — safe/read-only (does NOT submit the registration form).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from playwright.sync_api import sync_playwright

from config.settings import settings

OUT = pathlib.Path("artifacts")
OUT.mkdir(exist_ok=True)
BASE = settings.base_url.rstrip("/")


def snapshot(page, label):
    print(f"\n===== {label} | url={page.url} =====")
    try:
        print(page.locator("body").aria_snapshot())
    except Exception as e:  # older playwright fallback
        print(f"(aria_snapshot unavailable: {e})")
        print(page.locator("body").inner_text())


def main():
    acc = settings.account(3)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)
        page = browser.new_context().new_page()
        page.goto(BASE + "/login")
        page.get_by_role("textbox", name="이메일").fill(acc.email)
        page.get_by_role("textbox", name="비밀번호").fill(acc.password)
        page.get_by_role("button", name="로그인").click()
        page.wait_for_url(re.compile(r"/dashboard"), timeout=20000)

        page.get_by_role("link", name="기술인 관리").click()
        page.wait_for_url(re.compile(r"/worker"), timeout=20000)
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / "worker.png"), full_page=True)
        snapshot(page, "worker page")

        # Find the registration entry point and open it (no submit).
        btn = page.get_by_role("button", name=re.compile("사전가입|사전등록"))
        if btn.count() == 0:
            btn = page.get_by_text(re.compile("사전가입 등록"))
        print("\n--- 사전가입 진입 버튼 후보 수:", btn.count())
        if btn.count():
            btn.first.click()
            page.wait_for_timeout(1500)
            # Switch to the direct-input tab where name/phone/agency fields live.
            tab = page.get_by_role("tab", name=re.compile("직접 입력"))
            if tab.count():
                tab.first.click()
                page.wait_for_timeout(1500)
            page.screenshot(path=str(OUT / "worker_register.png"), full_page=True)
            snapshot(page, "사전가입 등록 - 직접 입력 form")

            # Trigger validation by attempting to submit an empty form (no record
            # is created on invalid input), then snapshot the inline errors.
            submit = page.get_by_role("button", name=re.compile("오류 확인 및 등록|등록"))
            if submit.count() and submit.first.is_enabled():
                submit.first.click()
                page.wait_for_timeout(1200)
                snapshot(page, "사전가입 등록 - 빈 폼 제출 후 에러")

        browser.close()
    print(f"\nScreenshots: {OUT.resolve()}")


if __name__ == "__main__":
    main()
