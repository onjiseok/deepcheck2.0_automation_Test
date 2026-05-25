"""Diagnostic: log in (level 3) and dump the 미측정 현황(/measure) page structure
so its filters/list/columns can be confirmed for test coverage.

Run (with .env configured):
    python scripts/inspect_measure.py

Prints a concise summary (controls + table headers) and saves the full aria
snapshot to artifacts/measure.txt plus a screenshot. Throwaway, read-only.
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


def main():
    acc = settings.account(3)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        page = browser.new_context().new_page()
        page.goto(BASE + "/login")
        page.get_by_role("textbox", name="이메일").fill(acc.email)
        page.get_by_role("textbox", name="비밀번호").fill(acc.password)
        page.get_by_role("button", name="로그인").click()
        page.wait_for_url(re.compile(r"/dashboard"), timeout=20000)

        page.get_by_role("link", name="미측정 현황").click()
        page.wait_for_url(re.compile(r"/measure"), timeout=20000)
        page.wait_for_timeout(3000)
        page.screenshot(path=str(OUT / "measure.png"), full_page=True)

        main_region = page.get_by_role("main")
        print(f"\n===== 미측정 현황 | url={page.url} =====")
        print("\n--- 제목/문단 ---")
        for h in main_region.get_by_role("heading").all():
            print("heading:", h.inner_text().replace("\n", " "))
        print("\n--- 탭 ---")
        for t in main_region.get_by_role("tab").all():
            print("tab:", t.inner_text().replace("\n", " "))
        print("\n--- 라디오/스위치/콤보 ---")
        for r in main_region.get_by_role("radio").all():
            print("radio:", r.inner_text().replace("\n", " "))
        for c in main_region.get_by_role("combobox").all():
            print("combobox:", c.inner_text().replace("\n", " "))
        print("\n--- 버튼 ---")
        for b in main_region.get_by_role("button").all():
            txt = b.inner_text().replace("\n", " ").strip()
            if txt:
                print(f"button: {txt!r} enabled={b.is_enabled()}")
        print("\n--- 테이블 컬럼 헤더 ---")
        for ch in main_region.get_by_role("columnheader").all():
            print("col:", ch.inner_text().replace("\n", " "))

        (OUT / "measure.txt").write_text(main_region.aria_snapshot(), encoding="utf-8")
        print(f"\n전체 스냅샷: {OUT / 'measure.txt'}")
        browser.close()
    print(f"Screenshot: {(OUT / 'measure.png').resolve()}")


if __name__ == "__main__":
    main()
