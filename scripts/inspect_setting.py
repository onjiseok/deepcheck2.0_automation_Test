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
        # Walk each settings sub-tab and dump its url + structure summary.
        for tab in ("기본 설정", "설문조사", "알림 관리", "기기 관리"):
            link = page.get_by_role("link", name=tab, exact=True)
            if not link.count():
                print(f"\n##### {tab}: 링크 없음 #####")
                continue
            link.first.click()
            page.wait_for_timeout(2500)
            slug = tab.replace(" ", "")
            print(f"\n##### [{tab}] url={page.url} #####")
            print("switch:", region.get_by_role("switch").count(),
                  "| radio:", region.get_by_role("radio").count(),
                  "| combobox:", region.get_by_role("combobox").count(),
                  "| 저장:", region.get_by_role("button", name="저장", exact=True).count(),
                  "| 취소:", region.get_by_role("button", name="취소", exact=True).count())
            print("--- heading ---")
            for h in region.get_by_role("heading").all():
                t = h.inner_text().replace("\n", " ").strip()
                if t:
                    print("  h:", t)
            print("--- 주요 버튼(텍스트 있는 것) ---")
            seen = set()
            for b in region.get_by_role("button").all():
                t = b.inner_text().replace("\n", " ").strip()
                if t and t not in seen and t not in ("저장", "취소"):
                    seen.add(t)
                    print(f"  btn: {t!r}")
            (OUT / f"setting_{slug}.txt").write_text(region.aria_snapshot(), encoding="utf-8")

        print(f"\n전체 스냅샷: artifacts/setting_<탭>.txt")
        browser.close()
    print(f"Screenshot: {(OUT / 'setting.png').resolve()}")


if __name__ == "__main__":
    main()
