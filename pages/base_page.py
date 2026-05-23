from __future__ import annotations

from playwright.sync_api import Page


class BasePage:
    """Base for Page Objects. Holds the Playwright page and shared helpers."""

    path = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> "BasePage":
        self.page.goto(self.path)
        return self
