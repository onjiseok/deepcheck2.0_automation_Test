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


def snapshot(target, label):
    print(f"\n===== {label} =====")
    try:
        print(target.aria_snapshot())
    except Exception as e:  # older playwright fallback
        print(f"(aria_snapshot unavailable: {e})")
        print(target.inner_text())


# Clearly-fake phone (per QA instruction): never a real contact, and rows are
# always kept invalid so registration never completes (no SMS attempt).
FAKE_PHONE_SHORT = "010"          # too short -> length error
PROBE_PHONE = "4445030807606"      # 13 digits, fake


def main():
    acc = settings.account(3)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_context().new_page()
        page.goto(BASE + "/login")
        page.get_by_role("textbox", name="이메일").fill(acc.email)
        page.get_by_role("textbox", name="비밀번호").fill(acc.password)
        page.get_by_role("button", name="로그인").click()
        page.wait_for_url(re.compile(r"/dashboard"), timeout=20000)

        page.get_by_role("link", name="기술인 관리").click()
        page.wait_for_url(re.compile(r"/worker"), timeout=20000)
        page.wait_for_timeout(2500)

        page.get_by_role("button", name=re.compile("사전가입")).first.click()
        page.wait_for_timeout(1200)
        page.get_by_role("tab", name=re.compile("직접 입력")).first.click()
        page.wait_for_timeout(1200)
        dialog = page.get_by_role("dialog")

        phone = page.get_by_role("textbox", name="전화번호 2행")
        name = page.get_by_role("textbox", name="이름 2행")
        agency = page.get_by_role("textbox", name="협력사 2행")

        # (1) Input-restriction probes (NO submit). Type mixed junk and read back
        # what the field actually keeps.
        phone.click()
        phone.press_sequentially("abc12!@34가56", delay=30)
        name.click()
        name.press_sequentially("12!@김영희#", delay=30)
        print("\n--- 입력 제한 결과 (제출 안 함) ---")
        print(f"전화번호 입력 'abc12!@34가56' -> 실제값: {phone.input_value()!r}")
        print(f"이름     입력 '12!@김영희#'    -> 실제값: {name.input_value()!r}")

        # (2) Error-table probe. Keep the row INVALID (short phone + 1-char name +
        # unregistered agency) so nothing registers, then read the error table.
        phone.fill("")
        phone.press_sequentially(FAKE_PHONE_SHORT, delay=30)
        name.fill("")
        name.press_sequentially("김", delay=30)
        agency.click()
        agency.press_sequentially("존재하지않는협력사_QA", delay=20)
        page.wait_for_timeout(300)
        submit = dialog.get_by_role("button", name="오류 확인 및 등록", exact=True)
        print("\n--- 제출 버튼 enabled?:", submit.is_enabled())
        if submit.is_enabled():
            submit.click()
            page.wait_for_timeout(1500)
        page.screenshot(path=str(OUT / "worker_register_errors.png"), full_page=True)

        # Concise result only (full snapshot saved to file to avoid huge stdout).
        print("\n--- 제출 결과 요약 ---")
        try:
            print("alert:", dialog.get_by_role("alert").inner_text())
        except Exception as e:
            print(f"(alert 없음: {e})")
        print("--- 에러 테이블 행 ---")
        for r in dialog.get_by_role("row").all():
            t = r.inner_text().replace("\n", " | ").strip()
            if any(k in t for k in ("오류 내용", "전화번호", "이름", "협력사")) and "예)" not in t:
                print(t)
        (OUT / "worker_register_errors.txt").write_text(
            dialog.aria_snapshot(), encoding="utf-8"
        )
        print(f"\n전체 스냅샷: {OUT / 'worker_register_errors.txt'}")

        browser.close()
    print(f"Screenshots: {OUT.resolve()}")


if __name__ == "__main__":
    main()
