from __future__ import annotations

import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage

# Confirmed landmarks (from the post-login dashboard screenshot):
#   전체 기술인 수 / 전체 협력사 수 / 측정 현황 / 총 측정자 수, and a
#   "yyyy.MM.dd HH:mm" data-reference timestamp in the header.
# Card titles for sections only seen in the TC sheet (시스템 공지, 가입 승인 대기,
# 보정 만료 예정, 사용자 통계 ...) are inferred and need a verification run.


class DashboardPage(BasePage):
    path = "/dashboard"

    NAV_ITEMS = (
        "대시보드",
        "기술인 관리",
        "미측정 현황",
        "설문 결과",
        "소속업체 관리",
        "계정 관리",
        "설정",
    )

    def text(self, value: str) -> Locator:
        return self.page.get_by_text(value)

    def nav_link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name)

    @property
    def data_timestamp(self) -> Locator:
        return self.page.get_by_text(re.compile(r"\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}"))
