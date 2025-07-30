from datetime import datetime
from typing import Union, Literal, Optional

from playwright.sync_api import expect, Locator
from robotlibcore import keyword

from .base_context import BaseContext

from .utils import Robot



class DatePickerHandler(BaseContext):



    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('input datetime')
    def input_datetime(self, locator: Union[str, Locator], value: str):
        """
        Input datetime to a datetime picker

        *locator*: the Locator of the element

        *value*: the value to be entered
        """
        element = self.get_element(locator)
        element.evaluate("node => node.removeAttribute('readonly')")
        element.fill(value, force=True)
        self.get_element("xpath=//body").click()
        Robot().sleep(0.5)
        return value

    @keyword('datepicker should be correct')
    def datepicker_should_be_correct(self, locator: Union[str, Locator],
                                     state: Literal["enabled", "disabled"] = 'enabled',
                                     default: Optional[str] = None):
        """
        Verify the datetime picker is correct or not

        *locator*: the Locator of the element

        *state*: Whether ``enabled`` or ``disabled``

        *default*: Default value of the datepicker.
        """
        element = self.get_element(locator)
        # Verify state
        if state == 'enabled':
            expect(element).to_be_enabled()
        elif state == 'disabled':
            expect(element).to_be_disabled()
        # Verify default value
        if default is not None:
            expect(element).to_have_value(default)

    @keyword('actual date should be')
    def actual_date_should_be(self, locator: Union[str, Locator], expected_date: str,
                              input_format: str = "%Y-%m-%d",
                              displayed_format: str = "%d %b, %Y"):
        """
        Compare the datetime value on an element to the expected datetime

        *locator*: the Locator of the element

        *expected_date*: The expected datetime

        *input_format*: The format of the expected date to be parsed. Default ``"%Y-%m-%d"``

        *displayed_format*: The datetime format on the element to be parsed. Default ``"%d %b, %Y"``

        """
        actual_date = self.get_element(locator).input_value()
        if datetime.strptime(expected_date, input_format) != datetime.strptime(actual_date, displayed_format):
            raise AssertionError(f"Actual date: '{actual_date}' is different with expected date: '{expected_date}'")

    @keyword('actual date should not be')
    def actual_date_should_not_be(self, locator: Union[str, Locator], expected_date: str,
                                  input_format: str = "%Y-%m-%d",
                                  displayed_format: str = "%d %b, %Y"):
        """
        Compare the datetime value on an element to the expected datetime

        *locator*: the Locator of the element

        *expected_date*: The expected datetime

        *input_format*: The format of the expected date to be parsed. Default ``"%Y-%m-%d"``

        *displayed_format*: The datetime format on the element to be parsed. Default ``"%d %b, %Y"``

        """
        actual_date = self.get_element(locator).input_value()
        if datetime.strptime(expected_date, input_format) == datetime.strptime(actual_date, displayed_format):
            raise AssertionError(f"Actual date: '{actual_date}' is the same with expected date: '{expected_date}'")
