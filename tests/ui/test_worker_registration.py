"""기술인 관리(/worker) 테스트 — TC 시트 '기술인 관리'(TC_161~185) 매핑.

level-3 계정으로 실측한 DOM(scripts/inspect_worker.py)에 맞춘 비파괴 검증.
검증 테스트는 항상 '오류가 있는 행'만 제출해 등록 0건(=SMS 없음)을 보장한다.
건강리포트/상담일지/테이블 상호작용과 단독 입력검증(다른 필드가 유효해야 해
등록 위험)·정상 등록·파일 업로드는 grouped skip으로 문서화한다.
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

# 8자 미만이라 항상 검증 실패 → 등록되지 않음(=SMS 없음). 실재하지 않는 번호.
INVALID_SHORT_PHONE = "010"


@pytest.fixture
def worker(logged_in_page) -> WorkerPage:
    return WorkerPage(logged_in_page).open()


# --- 사전가입 등록 진입/구조 (비파괴) ---
@requires_login
@pytest.mark.smoke
def test_pre_signup_dialog_opens(worker):  # 사전가입 등록 진입(파일/직접 입력 탭)
    expect(worker.register_button).to_be_visible()
    worker.register_button.click()
    expect(worker.dialog).to_be_visible()
    expect(worker.tab("파일 업로드")).to_be_visible()
    expect(worker.tab("직접 입력")).to_be_visible()


@requires_login
def test_direct_input_fields_present(worker):  # TC_174_002 직접 입력(보정값 포함) 필드
    worker.open_registration()
    for label in WorkerPage.FIELD_LABELS:
        expect(worker.field(label, row=2)).to_be_visible()


@requires_login
def test_submit_disabled_when_empty(worker):  # TC_166_004 모든 필드 미입력 → 등록 불가
    worker.open_registration()
    expect(worker.submit_button).to_be_disabled()


# --- 전화번호 길이 검증: 짧으면 등록 차단 ---
@requires_login
def test_short_phone_blocks_registration(worker):
    # TC_167_002, TC_167_006, TC_167_012 (전화번호 10글자 미만 → 오류/등록 차단)
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
    expect(worker.error_cell("전화번호")).to_be_visible()
    expect(worker.error_cell("8자 이상 입력해 주세요.")).to_be_visible()


# =====================================================================
# 자동화 보류 (TC 시트 기술인 관리) — 사유별 그룹.
# =====================================================================
@requires_login
@pytest.mark.skip(reason="건강리포트 그래프/뱃지/보정값 dot = 측정 데이터 보유 기술인 필요 (TC_161_001, TC_161_002, TC_162_001, TC_162_002, TC_163_001, TC_163_002, TC_163_003, TC_163_004, TC_185_001)")
def test_health_report_graph():
    ...


@requires_login
@pytest.mark.skip(reason="건강리포트 상담내역/상담일지 = 기술인+상담 데이터 필요 (TC_164_001, TC_164_002, TC_164_003, TC_164_004, TC_164_005, TC_175_001, TC_175_002, TC_175_003, TC_175_004, TC_175_005, TC_178_001, TC_178_002, TC_178_003, TC_179_001, TC_179_002, TC_179_003)")
def test_health_report_consultation():
    ...


@requires_login
@pytest.mark.skip(reason="건강리포트 PDF/엑셀 다운로드·기간 설정·엑셀 템플릿 = 데이터+다운로드 핸들링 (TC_165_001, TC_165_002, TC_176_001, TC_176_002, TC_177_001, TC_177_002, TC_177_003, TC_177_004, TC_177_005, TC_184_001)")
def test_health_report_download_and_period():
    ...


@requires_login
@pytest.mark.skip(reason="테이블 열이동/측정위치/보정값/통합필터 = 기술인 데이터 필요 (TC_180_001, TC_181_001, TC_182_001, TC_183_001)")
def test_table_interactions():
    ...


@requires_login
@pytest.mark.skip(reason="전화번호 입력제한/형식/경계 = 단독검증 시 다른 필드가 유효해야 해 등록 위험, 전용 환경 필요 (TC_167_001, TC_167_003, TC_167_004, TC_167_005, TC_167_007, TC_167_008, TC_167_010, TC_167_011, TC_167_013, TC_167_014)")
def test_phone_input_restriction_and_boundary():
    ...


@requires_login
@pytest.mark.skip(reason="중복 전화번호 검증 = 사전 등록된 실데이터 의존 (TC_167_009, TC_167_015)")
def test_duplicate_phone_rejected():
    ...


@requires_login
@pytest.mark.skip(reason="이름 입력제한/에러/경계 = 단독검증 시 등록 위험, 전용 환경 필요 (TC_168_001, TC_168_002, TC_168_003, TC_168_004, TC_168_005, TC_168_006, TC_168_007, TC_168_008, TC_168_009, TC_168_010, TC_169_001, TC_169_002, TC_169_003, TC_169_004)")
def test_name_input_validation():
    ...


@requires_login
@pytest.mark.skip(reason="협력사명 입력/미등록 검증 = 데이터+단독검증 시 등록 위험 (TC_170_001, TC_170_002, TC_170_003, TC_170_004, TC_170_005, TC_170_006, TC_171_001, TC_174_004)")
def test_agency_name_validation():
    ...


@requires_login
@pytest.mark.skip(reason="개별 필수 입력 누락 검증 = 단독검증 시 다른 필드 유효 필요, 등록 위험 (TC_166_001, TC_166_002, TC_166_003, TC_172_001, TC_172_002, TC_172_003, TC_172_004)")
def test_required_fields_missing():
    ...


@requires_login
@pytest.mark.skip(reason="파일 업로드 등록(누락/미등록 협력사 포함 엑셀) = 실제 등록/SMS, 파일 핸들링+전용 데이터 (TC_166_005, TC_171_002, TC_172_005)")
def test_file_upload_registration():
    ...


@requires_login
@pytest.mark.skip(reason="레벨4 [사전가입 등록] 버튼 표시/숨김·권한 연동 = 레벨4 권한+설정 (TC_173_001, TC_173_002, TC_173_003, TC_173_004)")
def test_level4_button_visibility():
    ...


@requires_login
@pytest.mark.skip(reason="정상 등록 = 실제 기술인 생성 + SMS 발송. 공유 환경 파괴적, 전용 데이터/계정 필요 (TC_174_003)")
def test_register_valid_worker():
    ...


@requires_login
@pytest.mark.skip(reason="직접 입력 행 삭제 = 등록 플로우 상호작용, 전용 데이터로 검증 (TC_174_001)")
def test_direct_input_row_delete():
    ...
