"""Diagnostic: log in (level 3) and dump the 설정(/setting/basic) page structure
so its sections/inputs/toggles/save controls can be confirmed for test coverage.

Run (with .env configured):
    python scripts/inspect_setting.py

Prints a concise summary and saves the full aria snapshot to
artifacts/setting.txt plus a screenshot. Throwaway, read-only: does NOT save
or change any setting.
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

        page.get_by_role("link", name="설정").click()
        page.wait_for_url(re.compile(r"/setting"), timeout=20000)
        page.wait_for_timeout(3000)
        page.screenshot(path=str(OUT / "setting.png"), full_page=True)

        region = page.get_by_role("main")
        print(f"\n##### 설정 | url={page.url} #####")
        print("\n--- 제목/탭/링크 ---")
        for h in region.get_by_role("heading").all():
            print("heading:", h.inner_text().replace("\n", " ").strip())
        for t in region.get_by_role("tab").all():
            print("tab:", t.inner_text().replace("\n", " ").strip())
        for lk in region.get_by_role("link").all():
            print("link:", lk.inner_text().replace("\n", " ").strip())
        print("\n--- 토글(switch)/체크박스/라디오 ---")
        print("switch 수:", region.get_by_role("switch").count())
        print("checkbox 수:", region.get_by_role("checkbox").count())
        for r in region.get_by_role("radio").all():
            print("radio:", r.inner_text().replace("\n", " ").strip())
        print("\n--- 콤보 / 입력 ---")
        for c in region.get_by_role("combobox").all():
            print("combobox:", c.inner_text().replace("\n", " ").strip())
        for tb in region.get_by_role("textbox").all():
            nm = tb.get_attribute("name") or tb.get_attribute("placeholder") or "?"
            print("textbox:", nm)
        for sb in region.get_by_role("spinbutton").all():
            nm = sb.get_attribute("name") or sb.get_attribute("placeholder") or "?"
            print("spinbutton:", nm)
        print("\n--- 버튼 ---")
        for b in region.get_by_role("button").all():
            txt = b.inner_text().replace("\n", " ").strip()
            if txt:
                print(f"button: {txt!r} enabled={b.is_enabled()}")

        (OUT / "setting.txt").write_text(region.aria_snapshot(), encoding="utf-8")
        print(f"\n전체 스냅샷: {OUT / 'setting.txt'}")
        browser.close()
    print(f"Screenshot: {(OUT / 'setting.png').resolve()}")


if __name__ == "__main__":
    main()
