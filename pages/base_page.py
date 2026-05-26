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
        attempts: int = 3,
        per_timeout: int = 8000,
    ) -> None:
        """Click a persistent nav link and wait for a destination-only element.

        The app is an SPA: a nav click issued before hydration (or one lost to a
        slow load) can be a no-op, so retry the click until the destination
        renders. The nav bar is present on every page, making re-clicks safe.
        """
        link = self.page.get_by_role("link", name=link_name)
        link.wait_for(state="visible", timeout=20000)
        last_error: Exception | None = None
        for _ in range(attempts):
            link.click()
            try:
                ready.wait_for(state="visible", timeout=per_timeout)
                return
            except PlaywrightTimeoutError as error:
                last_error = error
        raise last_error  # type: ignore[misc]
