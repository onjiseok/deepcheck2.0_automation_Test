from __future__ import annotations

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:
    """Base for Page Objects. Holds the Playwright page and shared helpers."""

    path = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> "BasePage":
        self.page.goto(self.path)
        return self

    def goto_via_nav(
        self,
        link_name: str,
        ready: Locator,
        *,
        attempts: int = 4,
        click_timeout: int = 12000,
        ready_timeout: int = 12000,
    ) -> None:
        """Click a persistent nav link and wait for a destination-only element.

        The app is an SPA on a sometimes-slow network: a nav click can be a
        no-op (issued before hydration) or hang (a loading overlay intercepts
        the click). Both the click and the readiness wait are bounded and
        retried; the nav bar is on every page, so re-clicks are safe.
        """
        link = self.page.get_by_role("link", name=link_name)
        last_error: Exception | None = None
        for _ in range(attempts):
            try:
                link.click(timeout=click_timeout)
                ready.wait_for(state="visible", timeout=ready_timeout)
                return
            except PlaywrightTimeoutError as error:
                last_error = error
        raise last_error  # type: ignore[misc]
