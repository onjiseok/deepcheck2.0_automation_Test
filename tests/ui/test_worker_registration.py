"""기술인 관리 - 사전가입자 등록 검증 테스트.

TC 시트 'Deep check 2.0(웹)' 기술인 사전가입 등록 항목에서 파생.
모든 케이스는 level-3 계정으로 실측한 DOM(scripts/inspect_worker.py)에 맞춰
작성했다.

SAFETY 원칙
- 실제 등록(정상 행 제출)은 SMS 발송 + 공유 환경 데이터 오염을 유발하므로
  자동화하지 않는다(skip).
- 검증 테스트는 항상 '오류가 있는 행'만 제출한다. 오류 행은 등록되지 않으므로
  (정상 등록 0명) SMS 시도가 발생하지 않는다.
- 전화번호가 필요한 곳에는 실재하지 않는 가짜 값만 사용한다.
"""
import re

import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.worker_page import WorkerPage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)

# 8자 미만이라 항상 검증 실패 → 등록되지 않음(=SMS 없음). 실제 번호가 아니다.
INVALID_SHORT_PHONE = "010"


@pytest.fixture
def worker(logged_in_page) -> WorkerPage:
    return WorkerPage(logged_in_page).open()


# --- 진입/구조 (비파괴) ---
@requires_login
@pytest.mark.smoke
def test_pre_signup_dialog_opens(worker):
    expect(worker.register_button).to_be_visible()
    worker.register_button.click()
    expect(worker.dialog).to_be_visible()
    expect(worker.tab("파일 업로드")).to_be_visible()
    expect(worker.tab("직접 입력")).to_be_visible()


@requires_login
def test_direct_input_fields_present(worker):
    worker.open_registration()
    for label in WorkerPage.FIELD_LABELS:
        expect(worker.field(label, row=2)).to_be_visible()


@requires_login
def test_submit_disabled_when_empty(worker):
    worker.open_registration()
    expect(worker.submit_button).to_be_disabled()


# --- 전화번호 유효성: 8자 미만 → 등록 차단 (비파괴) ---
@requires_login
def test_short_phone_blocks_registration(worker):
    worker.open_registration()
    worker.fill_row(
        2,
        phone=INVALID_SHORT_PHONE,
        name="김",
        agency="존재하지않는협력사_QA",
    )
    expect(worker.submit_button).to_be_enabled()
    worker.submit()

    # 정상 등록 0명 = 어떤 기술인도 생성되지 않음(SMS 시도 없음)
    expect(worker.result_summary()).to_contain_text("등록되지 않은 기술인: 1명")
    expect(worker.dialog.get_by_text(re.compile(r"등록된 기술인: 0명"))).to_be_visible()
    # 에러 테이블에 전화번호 길이 오류가 노출
    expect(worker.error_cell("전화번호")).to_be_visible()
    expect(worker.error_cell("8자 이상 입력해 주세요.")).to_be_visible()


# --- 자동화 보류 (등록 완료 = 파괴적/SMS 발송) ---
@requires_login
@pytest.mark.skip(reason="정상 등록 = 실제 기술인 생성 + SMS 발송. 공유 환경 파괴적, 전용 데이터/계정 필요 (TC_174_003)")
def test_register_valid_worker():
    ...


@requires_login
@pytest.mark.skip(reason="중복 전화번호 검증은 사전 등록된 실데이터 의존. 전용 픽스처 필요 (TC_167_009)")
def test_duplicate_phone_rejected():
    ...


@requires_login
@pytest.mark.skip(reason="엑셀 파일 업로드 등록 = 실제 등록/SMS 발생. 파일 업로드 핸들링 + 전용 데이터 필요")
def test_file_upload_registration():
    ...
