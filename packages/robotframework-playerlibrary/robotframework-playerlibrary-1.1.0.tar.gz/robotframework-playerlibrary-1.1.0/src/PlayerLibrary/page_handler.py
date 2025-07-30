import base64
from typing import Union, List

from playwright.sync_api import expect, Locator
from robotlibcore import keyword
from .base_context import BaseContext
from .utils import Robot
from .custom_locator import *


class PageHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('get all data of similar html elements')
    def get_all_data_of_similar_html_elements(self, locator: Union[str, Locator]) -> List[str]:
        """
        Return a list of elements' texts of similar ones

        *locator*: the locator of the element

        *Return type*: list of ``str``

        """
        elements = self.get_element(locator, get_all=True)
        return [element.text_content() for element in elements]

    @keyword('text should be visible')
    def text_should_be_visible(self, *texts):
        """
        Verify the texts displaying on the page

        *texts*: The pieces of texts
        """
        for text in texts:
            # element = self.get_element(f'//body//*[not(self::script)][contains(.,"{text}")]')
            elements =  self.page.get_by_text(text).all()
            for ele in elements:
                if ele.is_visible():
                    return
            raise AssertionError(f"The text `{text}` is not visible.")

    @keyword('text should not be visible')
    def text_should_not_be_visible(self, *texts):
        """
        Verify the texts not displaying on the page

        *texts*: The pieces of texts
        """
        for text in texts:
            # element = self.get_element(f'//body//*[not(self::script)][contains(.,"{text}")]')
            elements =  self.page.get_by_text(text).all()
            if not elements:
                return
            else:
                for ele in elements:
                    if not ele.is_visible():
                        return
            raise AssertionError(f"The text `{text}` is still visible.")

    @keyword('texts should be visible')
    def texts_should_be_visible(self, texts: list):
        """
        Verify the texts displaying on the page

        *texts*: The list of texts
        """
        # text_node = "text()" if not deep_scan else "."
        for text in texts:
            # element = self.get_element(f'//body//*[not(self::script)][contains({text_node},"{text}")]')
            elements =  self.page.get_by_text(text).all()
            for ele in elements:
                if ele.is_visible():
                    return
            raise AssertionError(f"The text `{text}` is not visible.")

    @keyword('texts should not be visible')
    def texts_should_not_be_visible(self, texts: list):
        """
        Verify the texts not displaying on the page

        *texts*: The list of texts
        """
        # text_node = "text()" if not deep_scan else "."
        for text in texts:
            # element = self.get_element(f'//body//*[not(self::script)][contains({text_node},"{text}")]')
            elements =  self.page.get_by_text(text).all()
            if not elements:
                return
            else:
                for ele in elements:
                    if not ele.is_visible():
                        return
            raise AssertionError(f"The text `{text}` is still visible.")

    @keyword('Page should have')
    def page_should_have(self, *items):
        """
        Verify the page contains expected elements or texts

        *items*: Can be both strings and locators
        """
        for item in items:
            if item.startswith(ALL_PREFIXES):
                self.page_should_have_element(item)
            else:
                self.text_should_be_visible(item)

    @keyword('page should not have')
    def page_should_not_have(self, *items):
        """
        Verify the page does not contain expected elements or texts

        *items*: Can be both strings and locators
        """
        for item in items:
            if item.startswith(ALL_PREFIXES):
                self.page_should_not_have_element(item)
            else:
                self.text_should_not_be_visible(item)

    @keyword('page should be blank')
    def page_should_be_blank(self):
        """
        Verify the page contains nothing
        """
        expect(self.page).to_have_url("about:blank")

    @keyword('page should have element')
    def page_should_have_element(self, locator: Union[str, Locator]) -> Locator:
        """
        Verify the page contains expected element

        *locator*: the locator of the element

        *Return type*: ``playwright.sync_api.Locator`` object
        """
        element = self.get_element(locator)
        expect(element).to_be_visible()
        return element

    @keyword('page should not have element')
    def page_should_not_have_element(self, locator: Union[str, Locator], recheck_timeout=2):
        """
        Verify the page does not contain expected element

        *locator*: the locator of the element

        *recheck_timeout*: the amount of time in seconds to recheck the condition one more time
        """
        element = self.get_element(locator)
        expect(element).to_be_hidden()
        Robot().sleep(recheck_timeout)
        expect(element).to_be_hidden()

    @keyword('page should be redirected to')
    def page_should_be_redirected_to(self, url: str):
        """
        Make sure the page redirects to the expected url

        *url*: the target url
        """
        expect(self.page).to_have_url(url)

    @keyword('alert should be shown')
    def alert_should_be_shown(self, content: str, locator: Union[str, Locator]):
        """
        Verify the alert showing on the browser after clicking on an element

        *locator*: the element to be clicked on

        *content*: the content of the dialog
        """
        with self.page.expect_event("dialog") as new_dialog_info:
            self.get_element(locator).click()
        dialog = new_dialog_info.value
        assert dialog.message == content
        dialog.dismiss()

    @keyword('capture screenshot')
    def capture_screenshot(self):
        """
        Capture the screenshot and automatically embed it into the Robot report html file using base64 image format
        """
        image_bytes = self.page.screenshot(full_page=True)
        image_source = base64.b64encode(image_bytes).decode('utf-8')
        image = f"""
        <html>
            <head>
                <style>
                img.one {{
                  height: 75%;
                  width: 75%;
                }}
                </style>
            </head>
            <body>
                <img class="one" src="data:image/png;base64, {image_source}">
            </body>
        </html>   
        """
        Robot().log(message=image, html=True)

    @keyword('get page source')
    def get_page_source(self) -> str:
        """
        Get the whole source of the page as string

        *return type*: ``str``
        """
        return self.page.content()

    @keyword('reload whole page')
    def reload_whole_page(self):
        """
        Reload the whole page
        """
        self.page.reload()

    @keyword('html title should be')
    def html_title_should_be(self, title: str):
        """
        Verify the title of the html page matching the expected one or not

        *title*: expected title
        """
        expect(self.page).to_have_title(title)

    @keyword('go back to previous page')
    def go_back_to_previous_page(self):
        """
        Go back to the previous page
        """
        self.page.go_back()

    @keyword("text having correct amount value")
    def text_having_correct_amount_value(self, text: str, amount):
        """

        :param text: Something like "I have the payout of {abc} will be refunded tomorrow". Should include the
        curly bracket here
        :param amount: The actual amount which will be replaced into {abc}

        """
        text = re.sub(r'(?<=\{).*(?=})', amount, text)
        text = text.replace("{", "").replace("}", "")
        self.page_should_have(text)

    @keyword('upload file')
    def upload_file(self, file_path: str, locator: Union[str, Locator] = '//input[@type="file"]'):
        """
        Handle the upload file function. Locator must point to the element having 'type=file' attribute

        *locator*: the locator of the element
        """
        self.get_element(locator).set_input_files(file_path)

    @keyword('scroll to element with additional alignment')
    def scroll_to_element_with_additional_alignment(self, locator: Union[str, Locator], alignment: str = 'true'):
        """
        scroll the page using Javascript snippet to the target element

        *locator*: the locator of the element

        *alignment*: the additional scroll behavior:

        True - the top of the element will be aligned to the top of the visible area of the scrollable ancestor

        False - the bottom of the element will be aligned to the bottom of the visible area of the scrollable ancestor

        If omitted, it will scroll to the top of the element
        """
        element = self.get_element(locator)
        element.evaluate(f"node => node.scrollIntoView({alignment});")

    @keyword('scroll right')
    def scroll_right(self):
        """
        scroll the page to the right hand side using Javascript snippet
        """
        self.page.evaluate("window.scrollTo(document.body.scrollWidth,document.body.scrollHeight);")

    @keyword('scroll down')
    def scroll_down(self):
        """
        scroll the page down using Javascript snippet
        """
        self.page.evaluate("window.scrollTo(0,document.body.scrollHeight);")

    @keyword('should be downloaded normally')
    def should_be_downloaded_normally(self, locator: Union[str, Locator]) -> str:
        """
        Verify the file can be downloaded normally

        Return the downloaded file's path

        *locator*: the locator of the element

        *Return type*: ``str``
        """
        with self.page.expect_download() as download_info:
            self.get_element(locator).click()
        download = download_info.value
        return download.path()

    @keyword('switch to previous page')
    def switch_to_previous_page(self):
        """
        Switch to the previous page
        """
        if len(self.context.pages)<2:
            raise RuntimeError("There's only 1 page opened in the current context")
        self.page = self.context.pages[-2]
        self.page.bring_to_front()

    @keyword('switch to latest page')
    def switch_to_latest_page(self):
        """
        Switch to a latest-opened page
        """
        if len(self.context.pages)<2:
            raise RuntimeError("There's only 1 page opened in the current context")
        self.page = self.context.pages[-1]
        self.page.bring_to_front()

    @keyword('switch to specific page')
    def switch_to_specific_page(self, page_index:int):
        """
        Switch to a specific page using its index

        *page_index*: the index of the target page
        """
        if len(self.context.pages)<2:
            raise RuntimeError("There's only 1 page opened in the current context")
        self.page = self.context.pages[page_index]
        self.page.bring_to_front()

    def _get_latest_page(self):
        return self.context.pages[-1]

    @keyword('go to url')
    def go_to_url(self, url: str, secure: bool =True):
        """
        Go to the url

        *url*: the target url to go

        *secure*: if enabled, using https instead of http
        """
        if secure:
            url = url.replace("http://", "https://")
        self.page.goto(url)

    @keyword('url should be')
    def url_should_be(self, url: str):
        """
        Verify current url matching expected url

        *url*: expected url
        """
        expect(self.page).to_have_url(url)

    @keyword('get current url')
    def get_current_url(self) -> str:
        """
        get current url string

        *Return type*: ``str``
        """
        return self.page.url