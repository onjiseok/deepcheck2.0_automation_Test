# Deep check 2.0 웹 자동화 — 진행 기록

최종 업데이트: 2026-05-29

## 개요
deepcheck 2.0 웹 관리자(dev: https://dev.deepcheck.deep-medi.com) UI E2E 자동화.
- 스택: Playwright(pytest-playwright) + pytest, Page Object 패턴
- 대상 계정: level-3(현장관리자) 기본. `.env`에 L1~L4 설정 가능
- 결과 리포팅: InfluxDB → Grafana (docker-compose, 아래 "다음 단계")

## 비파괴 원칙
공유 dev 환경이라 **데이터 변경/발송/삭제 케이스는 자동화하지 않고** 사유와 함께
skip으로 문서화한다. 검증 테스트는 항상 "오류가 남는 입력"만 제출해 실제 등록/
발송이 일어나지 않게 한다(예: 사전가입은 8자 미만 전화번호로 등록 0건 보장).

## 현재 스위트
- Page objects: `pages/` — login, dashboard, worker, measure, survey, agency,
  account, setting (+ base_page 공통 nav 재시도 헬퍼)
- Tests: `tests/ui/` — login, dashboard, worker_registration, measure, survey,
  agency, account, setting (+ smoke)
- 진단 스크립트: `scripts/inspect_*.py` (각 화면 DOM 실측, 읽기 전용)
- TC 커버리지 매퍼: `scripts/tc_coverage.py` (deepcheck_TC.xlsx 대조)

## TC 매핑 현황 (웹 시트 996건)
`python scripts/tc_coverage.py` 기준: **automated 78 / skipped 724 / missing 194**

0 missing 완료 화면(10):
- 로그인(25/57), 대시보드(16/47), 기술인 관리(5/89), 측정현황(9/64),
  설문결과(5/39), 소속업체 관리(5/50), 계정 관리(10/62),
  기본설정(1/121), 설문조사관리(1/114), 알림관리(1/81)

남은 화면(missing):
- 협력사 등록하기 113 (비로그인 `/register/request` 플로우)
- 기기 관리 53 (설정 탭, 현재 범위 제외)
- 네비게이션바 26
- 공통 2

## 실행
```bash
pytest tests/ui -v          # 전체 UI
pytest tests/ui/test_measure.py -v
python scripts/tc_coverage.py   # TC 커버리지 집계 (artifacts/tc_coverage.csv)
```

## 다음 단계
1. InfluxDB/Grafana 연동 활성화 (docker-compose + .env INFLUX_URL/TOKEN)
2. 남은 화면 TC 매핑(네비게이션바 → 협력사 등록하기)
3. 전용 테스트 데이터/계정 확보 시 skip 케이스(등록/수정/삭제/발송) 자동화
4. 메일/SMS 수신 검증(테스트 메일박스)으로 비밀번호 재설정·인증 플로우 자동화
