from typing import Union, Literal

from playwright.sync_api import expect, Locator
from robotlibcore import keyword
from .base_context import BaseContext



class ButtonHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('button should be enabled')
    def button_should_be_enabled(self, locator: Union[str, Locator]):
        """
        Verify the button with the ``locator`` to be enabled or not

        *locator*: the Locator of the button
        """
        element = self.get_element(locator)
        expect(element).to_be_enabled()

    @keyword('button should be disabled')
    def button_should_be_disabled(self, locator: Union[str, Locator]):
        """
        Verify the button with the ``locator`` to be disabled or not

        *locator*: the Locator of the button
        """
        element = self.get_element(locator)
        expect(element).to_be_disabled()

    @keyword('button should be correct')
    def button_should_be_correct(self, locator: Union[str, Locator], state: Literal["enabled", "disabled"] = 'enabled'):
        """
        Verify the button with the ``locator`` to be in correct state or not

        *locator*: the Locator of the button

        *state*: whether `enabled` or `disabled`
        """
        element = self.get_element(locator)
        self.button_should_be_enabled(element) if state.lower() == 'enabled' else self.button_should_be_disabled(element)

    @keyword('click button')
    def click_button(self, locator: Union[str, Locator], force: bool = False):
        """
        Click to a button

        *locator*: the Locator of the button

        *force*: When enabled, bypass the usability to click on the target button
        """
        element = self.get_element(locator)
        element.click(force=force)
