"""Diagnostic: log in (level 3) and dump the 소속업체 관리(/agency) page
structure so its filters/list/columns and any create dialog can be confirmed
for test coverage.

Run (with .env configured):
    python scripts/inspect_agency.py

Prints a concise summary and saves the full aria snapshot to
artifacts/agency.txt plus a screenshot. Throwaway, read-only: does NOT
submit/create/edit/delete anything.
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


def summarize(region):
    for h in region.get_by_role("heading").all():
        print("heading:", h.inner_text().replace("\n", " ").strip())
    for t in region.get_by_role("tab").all():
        print("tab:", t.inner_text().replace("\n", " ").strip())
    for r in region.get_by_role("radio").all():
        print("radio:", r.inner_text().replace("\n", " ").strip())
    for c in region.get_by_role("combobox").all():
        print("combobox:", c.inner_text().replace("\n", " ").strip())
    for tb in region.get_by_role("textbox").all():
        nm = tb.get_attribute("name") or tb.get_attribute("placeholder") or "?"
        print("textbox:", nm)
    for b in region.get_by_role("button").all():
        txt = b.inner_text().replace("\n", " ").strip()
        if txt:
            print(f"button: {txt!r} enabled={b.is_enabled()}")
    for ch in region.get_by_role("columnheader").all():
        print("col:", ch.inner_text().replace("\n", " ").strip())


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

        page.get_by_role("link", name="소속업체 관리").click()
        page.wait_for_url(re.compile(r"/agency"), timeout=20000)
        page.wait_for_timeout(3000)
        page.screenshot(path=str(OUT / "agency.png"), full_page=True)

        region = page.get_by_role("main")
        print(f"\n##### 소속업체 관리 | url={page.url} #####")
        summarize(region)
        (OUT / "agency.txt").write_text(region.aria_snapshot(), encoding="utf-8")

        # Try opening a create dialog WITHOUT submitting, to learn its fields.
        create = page.get_by_role("button", name=re.compile("협력사 (등록|추가)|소속업체 (등록|추가)|등록|추가"))
        if create.count():
            try:
                create.first.click()
                page.wait_for_timeout(1500)
                dlg = page.get_by_role("dialog")
                if dlg.count():
                    page.screenshot(path=str(OUT / "agency_create.png"), full_page=True)
                    print("\n----- 등록 다이얼로그 -----")
                    summarize(dlg.first)
                    for tb in dlg.first.get_by_role("textbox").all():
                        nm = tb.get_attribute("name") or tb.get_attribute("placeholder") or "?"
                        print("dialog textbox:", nm)
                    (OUT / "agency_create.txt").write_text(
                        dlg.first.aria_snapshot(), encoding="utf-8"
                    )
            except Exception as e:
                print(f"(등록 다이얼로그 열기 실패: {e})")

        print(f"\n전체 스냅샷: {OUT / 'agency.txt'} (+ agency_create.txt if dialog)")
        browser.close()
    print(f"Screenshots: {OUT.resolve()}")


if __name__ == "__main__":
    main()
