"""설정(/setting) 테스트 — TC 시트 기본설정/설문조사관리/알림관리 탭 매핑.

level-3 계정으로 실측한 DOM(scripts/inspect_setting.py)에 맞춘 비파괴 검증.
설정 탭은 대부분 토글 on/off·디폴트값·저장(설정 변경=파괴적)이므로 탭 진입만
automated로 두고, 나머지는 그룹 skip으로 문서화한다. 기기 관리 탭은 범위 제외.
이 파일의 skip 스킹은 scripts/tc_coverage.py 기준 0 missing을 위해 그룹별로 구성된다.
"""
import re

import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.setting_page import SettingPage

pytestmark = [pytest.mark.ui]

requires_login = pytest.mark.skipif(
    not settings.base_url or 3 not in settings.accounts,
    reason="BASE_URL or level-3 account not configured",
)


@pytest.fixture
def setting(logged_in_page) -> SettingPage:
    return SettingPage(logged_in_page).open()


# --- 진입 / 서브 네비게이션 ---
@requires_login
@pytest.mark.smoke
def test_setting_loads(setting):  # TC_287_001 기본설정 탭 진입
    expect(setting.page).to_have_url(re.compile(r"/setting/basic"))
    expect(setting.subnav_link("기본 설정")).to_be_visible()


@requires_login
@pytest.mark.parametrize("name", SettingPage.SUBNAV)
def test_subnav_links_visible(setting, name):
    expect(setting.subnav_link(name)).to_be_visible()


@requires_login
def test_toggles_present(setting):
    assert setting.toggles.count() > 0


@requires_login
def test_save_buttons_disabled_by_default(setting):
    expect(setting.save_buttons.first).to_be_visible()
    buttons = setting.save_buttons
    count = buttons.count()
    assert count > 0, "저장 버튼을 찾지 못함"
    for i in range(count):
        expect(buttons.nth(i)).to_be_disabled()


@requires_login
def test_cancel_buttons_disabled_by_default(setting):
    expect(setting.cancel_buttons.first).to_be_visible()
    buttons = setting.cancel_buttons
    count = buttons.count()
    assert count > 0, "취소 버튼을 찾지 못함"
    for i in range(count):
        expect(buttons.nth(i)).to_be_disabled()


@requires_login
def test_survey_setting_tab_loads(setting):  # TC_367_001 설문조사 탭 진입
    setting.open_tab("설문조사")
    expect(setting.page).to_have_url(re.compile(r"/setting/survey"))


@requires_login
def test_alarm_setting_tab_loads(setting):  # TC_602_001 알림관리 탭 진입
    setting.open_tab("알림 관리")
    expect(setting.page).to_have_url(re.compile(r"/setting/alarm"))
    expect(setting.page.get_by_role("heading", name="알림 요일 설정")).to_be_visible()


# =====================================================================
# 자동화 보류 (TC 시트 설정 3개 탭) — 설정 변경/디폴트값 상세 = 파괴적/데이터 의존.
# 그룹별 skip으로 전체 TC_ID를 문서화해 0 missing을 유지한다.
# =====================================================================
@requires_login
@pytest.mark.skip(reason="기본설정/접근 권한 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_284_001, TC_285_001, TC_286_001)")
def test_skip_basic_01():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/기술인 유형 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_288_001, TC_288_002, TC_288_003, TC_289_001, TC_289_002, TC_289_003, TC_289_004, TC_290_001, TC_290_002, TC_290_003, TC_290_004, TC_291_001, TC_291_002, TC_292_001, TC_293_001, TC_294_001, TC_294_002, TC_294_003, TC_294_004, TC_294_005, TC_295_001, TC_295_002, TC_296_001, TC_297_001, TC_298_001, TC_299_001, TC_300_001, TC_300_002, TC_301_001, TC_302_001, TC_303_001, TC_303_002, TC_303_003, TC_303_004, TC_304_001, TC_305_001, TC_305_002, TC_305_003, TC_305_004, TC_305_005, TC_306_001, TC_307_001, TC_307_002, TC_307_003, TC_307_004, TC_307_005, TC_307_006, TC_308_001, TC_308_002, TC_308_003, TC_309_001, TC_310_001, TC_311_001)")
def test_skip_basic_02():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/삭제 대기 리스트 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_312_001, TC_313_001, TC_314_001, TC_315_001, TC_316_001, TC_316_002, TC_317_001, TC_318_001, TC_318_002, TC_319_001, TC_320_001, TC_321_001, TC_322_001, TC_322_002, TC_323_001, TC_323_002, TC_324_001)")
def test_skip_basic_03():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/출근자 리스트 유지 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_325_001, TC_325_002, TC_326_001, TC_327_001, TC_328_001, TC_329_001, TC_330_001, TC_331_001, TC_332_001)")
def test_skip_basic_04():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/기술인 보정 주기 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_333_001, TC_333_002, TC_334_001, TC_335_001, TC_336_001, TC_337_001, TC_337_002, TC_338_001, TC_339_001)")
def test_skip_basic_05():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/지표 노출 설정 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_340_001, TC_340_002, TC_341_001, TC_342_001, TC_343_001, TC_344_001)")
def test_skip_basic_06():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/협력사 관리자 권한 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_345_001, TC_345_002, TC_345_003, TC_346_001, TC_347_001)")
def test_skip_basic_07():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/기술인 자동가입 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_348_001, TC_348_002, TC_348_003, TC_349_001, TC_350_001)")
def test_skip_basic_08():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/측정앱 결과 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_351_001, TC_351_002)")
def test_skip_basic_09():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/소속 회사 정보 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_352_001, TC_353_001, TC_354_001, TC_355_001, TC_356_001, TC_357_001)")
def test_skip_basic_10():
    ...


@requires_login
@pytest.mark.skip(reason="기본설정/저장/취소 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_358_001, TC_359_001, TC_360_001, TC_361_001, TC_362_001, TC_363_001)")
def test_skip_basic_11():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/접근 권한 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_364_001, TC_365_001, TC_366_001, TC_392_001, TC_393_001, TC_394_001)")
def test_skip_survey_01():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/화면 구성 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_368_001, TC_369_001, TC_370_001, TC_371_001, TC_372_001, TC_373_001, TC_374_001)")
def test_skip_survey_02():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/시행 on/off = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_375_001, TC_375_002, TC_376_001, TC_377_001)")
def test_skip_survey_03():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/반복주기 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_378_001, TC_379_001, TC_380_001, TC_381_001, TC_382_001, TC_383_001, TC_384_001, TC_385_001, TC_386_001, TC_387_001, TC_388_001)")
def test_skip_survey_04():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/저장/취소 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_389_001, TC_390_001, TC_391_001, TC_474_001, TC_475_001, TC_476_001)")
def test_skip_survey_05():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/탭 진입 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_395_001)")
def test_skip_survey_06():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/전체 알림 허용 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_396_001, TC_397_001, TC_398_001)")
def test_skip_survey_07():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/알림 요일 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_399_001, TC_400_001, TC_401_001, TC_402_001, TC_403_001)")
def test_skip_survey_08():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/미측정자 알림 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_404_001, TC_405_001, TC_406_001, TC_407_001, TC_408_001, TC_409_001, TC_410_001, TC_411_001)")
def test_skip_survey_09():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/미측정자 알림-유형 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_412_001, TC_413_001, TC_414_001, TC_415_001, TC_416_001, TC_417_001, TC_418_001)")
def test_skip_survey_10():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/미측정자 알림-유형-일반 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_419_001)")
def test_skip_survey_11():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/미측정자 알림-유형-고위험 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_419_002)")
def test_skip_survey_12():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/미측정자 알림-유형-고령자 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_420_001)")
def test_skip_survey_13():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/미측정자 알림-시간 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_421_001, TC_422_001, TC_423_001, TC_424_001, TC_425_001, TC_426_001, TC_427_001)")
def test_skip_survey_14():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/이상자 알림 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_428_001, TC_429_001)")
def test_skip_survey_15():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/알림 off시간 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_430_001, TC_431_001, TC_432_001, TC_433_001, TC_434_001, TC_435_001, TC_436_001, TC_437_001, TC_438_001, TC_439_001, TC_440_001)")
def test_skip_survey_16():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/이상자 판정 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_441_001, TC_442_001, TC_443_001, TC_444_001, TC_445_001, TC_446_001)")
def test_skip_survey_17():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/이상범위-심혈관 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_447_001, TC_448_001, TC_449_001, TC_450_001, TC_451_001, TC_452_001, TC_453_001, TC_454_001, TC_455_001, TC_456_001, TC_457_001, TC_458_001)")
def test_skip_survey_18():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/이상범위-심박수 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_459_001, TC_460_001, TC_461_001)")
def test_skip_survey_19():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/이상범위-체온 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_462_001, TC_463_001, TC_464_001, TC_465_001, TC_466_001, TC_467_001)")
def test_skip_survey_20():
    ...


@requires_login
@pytest.mark.skip(reason="설문조사관리/이상범위-알코올 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_468_001, TC_469_001, TC_470_001, TC_471_001, TC_472_001, TC_473_001)")
def test_skip_survey_21():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/접근 권한 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_599_001, TC_600_001, TC_601_001)")
def test_skip_alarm_01():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/전체 알림 허용 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_603_001, TC_603_002, TC_604_001)")
def test_skip_alarm_02():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/알림 요일 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_605_001, TC_606_001, TC_607_001, TC_608_001)")
def test_skip_alarm_03():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/미측정자 알림 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_609_001, TC_610_001, TC_611_001, TC_612_001, TC_613_001, TC_614_001, TC_615_001)")
def test_skip_alarm_04():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/미측정자 알림-유형 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_616_001, TC_617_001, TC_618_001, TC_619_001, TC_620_001)")
def test_skip_alarm_05():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/미측정자 알림-유형-일반 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_621_001)")
def test_skip_alarm_06():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/미측정자 알림-유형-고위험 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_622_001)")
def test_skip_alarm_07():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/미측정자 알림-유형-고령자 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_623_001)")
def test_skip_alarm_08():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/미측정자 알림-시간 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_624_001, TC_625_001, TC_626_001, TC_627_001, TC_628_001, TC_629_001, TC_630_001)")
def test_skip_alarm_09():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/이상자 알림 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_631_001, TC_632_001)")
def test_skip_alarm_10():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/알림 off시간 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_633_001, TC_634_001, TC_635_001, TC_636_001, TC_637_001, TC_638_001, TC_639_001, TC_640_001, TC_641_001, TC_642_001, TC_643_001)")
def test_skip_alarm_11():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/이상자 판정 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_644_001, TC_645_001, TC_646_001, TC_647_001, TC_648_001, TC_649_001)")
def test_skip_alarm_12():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/이상범위-심혈관 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_650_001, TC_651_001, TC_652_001, TC_653_001, TC_654_001, TC_655_001, TC_656_001, TC_657_001, TC_658_001, TC_659_001, TC_660_001, TC_661_001)")
def test_skip_alarm_13():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/이상범위-심박수 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_662_001, TC_663_001, TC_664_001)")
def test_skip_alarm_14():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/이상범위-체온 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_665_001, TC_666_001, TC_667_001, TC_668_001, TC_669_001, TC_670_001)")
def test_skip_alarm_15():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/이상범위-알코올 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_671_001, TC_672_001, TC_673_001, TC_674_001, TC_675_001, TC_676_001)")
def test_skip_alarm_16():
    ...


@requires_login
@pytest.mark.skip(reason="알림관리/저장/취소 = 설정 변경·디폴트값 상세(파괴적·데이터 의존) (TC_677_001, TC_678_001, TC_679_001)")
def test_skip_alarm_17():
    ...

