from typing import Union, Optional, Literal

from playwright.sync_api import expect, Locator
from robotlibcore import keyword
from .base_context import BaseContext
from .utils import random_number_chars
from .utils import Robot


class TextboxHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('input into')
    def input_into(self, locator: Union[str, Locator], text: str, clear: bool = True, force: bool = False) -> str:
        """
        Input text into a textbox, return the inputted text

        *locator*: locator of the element

        *text*: the text to be inputted to the element

        *clear*: clear the current text on the textbox or not

        *force*: bypass the usability to input the text or not

        *Return Type*: ``str``
        """
        element = self.get_element(locator)
        if clear:
            element.fill('', force=force)
        element.fill(text, force=force)
        return text


    @keyword("input text by pressing key")
    def input_text_by_pressing_key(self, locator: Union[str, Locator], text: str, delay: int = 100) -> str:
        """
        Input text into a textbox using single key down signal. Return the inputted text

        *locator*: locator of the element

        *text*: the text to be inputted to the element

        *delay*: delay in each input, in milliseconds

        *Return type*: ``str``
        """
        self.get_element(locator).type(text, delay=delay)
        return text

    @keyword('clear text using backspace')
    def clear_text_using_backspace(self, locator: Union[str, Locator]):
        """
        Clear the text using the backspace button

        *locator*: locator of the element
        """
        element = self.get_element(locator)
        element.select_text()
        element.press("Backspace")

    @keyword('clear text')
    def clear_text(self, locator: Union[str, Locator]):
        """
        Clear the text in a textbox

        *locator*: locator of the element
        """
        self.get_element(locator).fill("")

    @keyword('maxlength should be')
    def maxlength_should_be(self, locator: Union[str, Locator], expected_maxlength: int):
        """
        Verify the maxlength of a textbox

        *locator*: locator of the element

        *expected_maxlength*: the expected maxlength of the textbox
        """
        element = self.get_element(locator)
        element.fill("")
        length = int(expected_maxlength) + 1
        string = random_number_chars(length)
        element.fill(string)
        Robot().should_be_equal_as_integers(len(element.input_value()), expected_maxlength)
        element.fill("")

    @keyword('textbox should be empty')
    def textbox_should_be_empty(self, locator: Union[str, Locator]):
        """
        Verify the textbox is empty

        *locator*: locator of the element
        """
        expect(self.get_element(locator)).to_have_value("")

    @keyword('Placeholder should be')
    def placeholder_should_be(self, locator: Union[str, Locator], expected_text: str):
        """
        Verify the placeholder of a textbox is equal to an expected text or not

        *locator*: locator of the element

        *expected_text*: expected text in the placeholder
        """
        expect(self.get_element(locator)).to_have_attribute("placeholder", expected_text)

    @keyword('textbox should be correct')
    def textbox_should_be_correct(self, locator: Union[str, Locator], state: Literal["enabled", "disabled"] = 'enabled',
                                  default: Optional[str] = None, maxlength: Optional[int] = None, is_numeric: bool = False):
        """
        Verify the textbox is correct or not

        *locator*: locator of the element

        *state*: whether ``enabled`` or ``disabled``

        *default*: default value of the texbox

        *maxlength*: maxlength of the textbox

        *is_numeric*: the textbox is numeric input or not
        """
        element = self.get_element(locator)
        default = default.replace(',', '') if is_numeric else default
        # Verify state
        if state == 'enabled':
            expect(element).to_be_enabled()
        elif state == 'disabled':
            expect(element).to_be_disabled()
        # Verify default value
        if default is not None:
            expect(element).to_have_value(default)
        # Verify Max-length
        if maxlength is not None:
            self.maxlength_should_be(element, maxlength)
