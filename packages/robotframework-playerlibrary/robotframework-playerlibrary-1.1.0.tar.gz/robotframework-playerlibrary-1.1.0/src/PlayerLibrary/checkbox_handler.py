from typing import Union, Literal
from playwright.sync_api import expect, Locator
from robotlibcore import keyword
from .base_context import BaseContext



class CheckboxHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('checkbox should be enabled')
    def checkbox_should_be_enabled(self, locator: Union[str, Locator]):
        """
        Verify the checkbox with the ``locator`` to be enabled

        *locator*: the Locator of the element
        """
        element = self.get_element(locator)
        expect(element).to_be_enabled()

    @keyword('checkbox should be disabled')
    def checkbox_should_be_disabled(self, locator: Union[str, Locator]):
        """
        Verify the checkbox with the ``locator`` to be disabled

        *locator*: the Locator of the element
        """
        element = self.get_element(locator)
        expect(element).to_be_disabled()

    @keyword('tick checkbox')
    def tick_checkbox(self, locator: Union[str, Locator]):
        """
        Select the checkbox. If it has been already checked, do nothing

        *locator*: the Locator of the element
        """
        element = self.get_element(locator)
        element.check()

    @keyword('untick checkbox')
    def untick_checkbox(self, locator: Union[str, Locator]):
        """
        Unselect the checkbox. If it has been already unchecked, do nothing

        *locator*: the Locator of the element
        """
        element = self.get_element(locator)
        element.uncheck()

    @keyword('checkbox should be checked')
    def checkbox_should_be_checked(self, locator: Union[str, Locator]):
        """
        Verify the checkbox is being checked

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).to_be_checked()

    @keyword('checkbox should not be checked')
    def checkbox_should_not_be_checked(self, locator: Union[str, Locator]):
        """
        Verify the checkbox is being unchecked

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).not_to_be_checked()

    @keyword('get current checkbox checking status')
    def get_current_checkbox_checking_status(self, locator: Union[str, Locator]) -> bool:
        """
        Return ``true`` if the checkbox is currently selected, else ``false``

        *locator*: the Locator of the element
        """
        return self.get_element(locator).is_checked()

    @keyword('checkbox should be correct')
    def checkbox_should_be_correct(self, locator: Union[str, Locator],
                                   state: Literal["enabled", "disabled"]='enabled',
                                   status: Literal["checked", "unchecked"]='unchecked'):
        """
        Verify if the checkbox is correct or not

        *locator*: the Locator of the element

        *state*: whether ``enabled`` or ``disabled``

        *status*: whether ``checked`` or ``unchecked``
        """
        element = self.get_element(locator)
        if state == 'enabled':
            expect(element).to_be_enabled()
        elif state == 'disabled':
            expect(element).to_be_disabled()
        if status == 'unchecked':
            expect(element).not_to_be_checked()
        elif status == 'checked':
            expect(element).to_be_checked()

    @keyword('select a radio option')
    def select_a_radio_option(self, locator: Union[str, Locator]):
        """
        Click to a radio button. If it's already checked, do nothing

        *locator*: the Locator of the element
        """
        radio = self.get_element(locator)
        if not radio.is_checked():
            radio.click()

    @keyword('radio button should be disabled')
    def radio_button_should_be_disabled(self, locator: Union[str, Locator]):
        """
        Verify the radio button is currently disabled

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).to_be_disabled()

    @keyword('radio button should be enabled')
    def radio_button_should_be_enabled(self, locator: Union[str, Locator]):
        """
        Verify the radio button is currently enabled

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).to_be_enabled()

    @keyword('radio button should be checked')
    def radio_button_should_be_checked(self, locator: Union[str, Locator]):
        """
        Verify the radio button is currently checked

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).to_be_checked()

    @keyword('radio button should not be checked')
    def radio_button_should_not_be_checked(self, locator: Union[str, Locator]):
        """
        Verify the radio button is currently unchecked

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).not_to_be_checked()

    @keyword('get current radio button checking status')
    def get_current_radio_button_checking_status(self, locator: Union[str, Locator]):
        """
        Return ``true`` if the radio button is currently selected, else ``false``

        *locator*: the Locator of the element
        """
        return self.get_element(locator).is_checked()

    @keyword('radio should be correct')
    def radio_should_be_correct(self, locator, state: Literal["enabled", "disabled"]='enabled',
                                status: Literal["checked", "unchecked"]='unchecked'):
        """
        Verify if the radio button is correct or not

        *locator*: the Locator of the element

        *state*: whether ``enabled`` or ``disabled``

        *status*: whether ``checked`` or ``unchecked``
        """
        element = self.get_element(locator)
        if state == 'enabled':
            expect(element).to_be_enabled()
        elif state == 'disabled':
            expect(element).to_be_disabled()
        if status == 'unchecked':
            expect(element).not_to_be_checked()
        elif status == 'checked':
            expect(element).to_be_checked()
