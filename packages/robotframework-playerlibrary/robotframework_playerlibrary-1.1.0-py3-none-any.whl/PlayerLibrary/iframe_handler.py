from typing import Union

from playwright.sync_api import expect, Locator
from robotlibcore import keyword
from .base_context import BaseContext
from .custom_locator import standardize_locator


class IframeHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('select iframe')
    def select_iframe(self, locator: Union[str, Locator]):
        """
        Enter an iframe on the page

        *locator*: the locator of the iframe
        """
        iframe = self.get_element(locator)
        self.iframe = iframe.content_frame

    @keyword("get iframe element")
    def get_iframe_element(self, locator: Union[str, Locator], get_all: bool = False):
        """
        Get the element via a Locator within an iframe

        *locator*: the locator pointed to the element

        *get_all*: if enabled, returns the list of similar elements. If disabled, only returns the first one
        """
        index = 1
        if isinstance(locator, Locator):
            return locator
        locator, index = standardize_locator(locator)
        print(f"Formatted locator is `{locator}`")
        print(f"Index of locator is `{index}`")
        return self.iframe.locator(locator).nth(index-1) if not get_all else self.iframe.locator(locator).all()

    @keyword('unselect iframe')
    def unselect_iframe(self):
        """
        Escape an iframe on the page

        *locator*: the locator of the iframe
        """
        self.iframe = None

    @keyword('iframe should contain')
    def iframe_should_contain(self, *texts):
        """
        Verify the iframe selected with `select iframe` containing some pieces of texts

        *texts*: expected texts
        """
        for text in texts:
            expect(self.iframe.get_by_text(text)).to_be_visible()

    @keyword('iframe should not contain')
    def iframe_should_not_contain(self, *texts):
        """
        Negative keyword of `iframe should contain`
        """
        for text in texts:
            expect(self.iframe.get_by_text(text)).to_be_hidden()

    @keyword('input on iframe')
    def input_on_iframe(self, locator: Union[str, Locator], text: str):
        """
        input to a textbox inside the iframe selected with `select iframe`

        *locator*: locator of the element

        *text*: The text to input to the textbox
        """
        self.get_iframe_element(locator).fill(text)

    @keyword('click on iframe')
    def click_on_iframe(self, locator: Union[str, Locator]):
        """
        click to an element inside the iframe selected with `select iframe`

        *locator*: locator of the element
        """
        self.get_iframe_element(locator).click()

    @keyword('tick on iframe')
    def tick_on_iframe(self, locator: Union[str, Locator]):
        """
        Tick to an checkbox inside the iframe selected with `select iframe`

        *locator*: locator of the element
        """
        self.get_iframe_element(locator).check()

    @keyword('untick on iframe')
    def untick_on_iframe(self, locator: Union[str, Locator]):
        """
        Untick to an checkbox inside the iframe selected with `select iframe`

        *locator*: locator of the element
        """
        self.get_iframe_element(locator).uncheck()

    @keyword('select value on iframe')
    def select_value_on_iframe(self, locator: Union[str, Locator], value: str):
        """
        Select a value from a dropdown inside the iframe selected with `select iframe`

        *locator*: locator of the element
        """
        self.get_iframe_element(locator).select_option(label=value)

    @keyword('iframe should have element')
    def iframe_should_have_element(self, locator: Union[str, Locator]):
        """
        Verify the iframe selected with `select iframe` containing an element

        *locator*: locator of the element
        """
        expect(self.get_iframe_element(locator)).to_be_visible()
