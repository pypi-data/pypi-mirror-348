from typing import Optional

from .base_context import BaseContext
from robotlibcore import keyword

class BrowserHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword("Setup custom locator and timeout")
    def setup_custom_locator_and_timeout(self):
        """
        Setup custom locator and timeout
        """
        self.setup_custom_locators()
        self.setup_assertion_timeout()

    @keyword('start blank browser')
    def start_blank_browser(self, browser: str = "chromium", headless: bool = False):
        """
        Start a blank browser

        *browser*: browser name: firefox, chromium, msedge, webkit...

        *headless*: enable the headless mode or not
        """
        self.browser = self.player.__getattribute__(browser)
        self.context = self.browser.launch(headless=headless).new_context()
        self.page = self.context.new_page()

    @keyword('start browser with url')
    def start_browser_with_url(self, url: str, browser: str = "chromium", headless: bool = False,
                               timeout: Optional[int] = 30000):
        """
        Start a blank browser then open a URL

        *url*: the URL to be opened

        *browser*: browser name: firefox, chromium, msedge, webkit...

        *headless*: enable the headless mode or not
        """
        self.browser = self.player.__getattribute__(browser)
        self.context = self.browser.launch(headless=headless).new_context()
        self.page = self.context.new_page()
        self.page.goto(url, timeout=timeout)


    @keyword('start new browser session')
    def start_new_browser_session(self, headless: bool = False, timeout: Optional[int] = 30000):
        """
        Reuse the current browser instance but open a completely new session by creating a new Playwright context

        *headless*: enable the headless mode or not
        """
        new_context = self.browser.launch(headless=headless).new_context()
        self.context.close()
        self.context = new_context
        self.page = self.context.new_page()
        self.page.reload(timeout=timeout)

    @keyword('quit all browsers')
    def quit_all_browsers(self):
        """
        Close all current browser instances
        """
        self.context.close()
        self.player.stop()
        BaseContext.playwright_context_manager = None




