from typing import Union

from playwright.sync_api import expect, Locator
from robotlibcore import keyword
from .base_context import BaseContext


class DropdownHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('dropdown should be enabled')
    def dropdown_should_be_enabled(self, locator: Union[str, Locator]):
        """
        Verify the dropdown is currently enabled

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).to_be_enabled()

    @keyword('dropdown should be disabled')
    def dropdown_should_be_disabled(self, locator: Union[str, Locator]):
        """
        Verify the dropdown is currently disabled

        *locator*: the Locator of the element
        """
        expect(self.get_element(locator)).to_be_disabled()

    @keyword('select value')
    def select_value(self, locator: Union[str, Locator], selected_value: str):
        """
        Select a value from a dropdown list

        *locator*: the Locator of the element

        *selected_value*: the value to be selected
        """
        self.get_element(locator).select_option(label=selected_value, force=True)

    @keyword('dropdown itemlist should be')
    def dropdown_itemlist_should_be(self, locator: Union[str, Locator], item_list: str):
        """
        Verify the dropdown having correct item list

        ``item_list`` needs to be separated with ';' for each value

        E.g: Robot;Agent;Sale;Customer

        *locator*: the Locator of the element

        *item_list*: The expected list of values, separated with ``;``
        """
        assert self.get_list_values(locator) == item_list.split(
            ";"), f'{self.get_list_values(locator)} is not equal to {item_list.split(";")}'

    @keyword('list item should be')
    def list_item_should_be(self, locator, *item_list: str):
        """
        Verify the dropdown having correct item list

        E.g: Robot;Agent;Sale;Customer

        *locator*: the Locator of the element

        *item_list*: The expected list of values
        """
        assert self.get_list_values(locator) == list(item_list), f'{self.get_list_values(locator)} is not equal to ' \
                                                                 f'{item_list}'

    @keyword('dropdown itemlist should contain')
    def dropdown_itemlist_should_contain(self, locator, item_list):
        it = iter(self.get_list_values(locator))
        assert all(item in it for item in item_list.split(";"))

    @keyword('dropdown itemlist should not contain')
    def dropdown_itemlist_should_not_contain(self, locator: Union[str, Locator], item_list):
        it = iter(self.get_list_values(locator))
        assert not all(item in it for item in item_list.split(";"))

    @keyword('dropdown current value should be')
    def dropdown_current_value_should_be(self, locator: Union[str, Locator], expected_value):
        value = self.get_element(locator).evaluate("select => select.options[select.selectedIndex].text")
        print(f"Current value is {value}")
        assert value == expected_value

    @keyword('dropdown current value should not be')
    def dropdown_current_value_should_not_be(self, locator: Union[str, Locator], expected_value):
        value = self.get_element(locator).evaluate("select => select.options[select.selectedIndex].text")
        print(f"Current value is {value}")
        assert value != expected_value

    @keyword('dropdown current value should contain')
    def dropdown_current_value_should_contain(self, locator: Union[str, Locator], expected_value):
        value = self.get_element(locator).evaluate("select => select.options[select.selectedIndex].text")
        print(f"Current value is {value}")
        assert expected_value in value

    @keyword('dropdown current value should not contain')
    def dropdown_current_value_should_not_contain(self, locator: Union[str, Locator], expected_value):
        value = self.get_element(locator).evaluate("select => select.options[select.selectedIndex].text")
        print(f"Current value is {value}")
        assert expected_value not in value

    @keyword('get current selected value')
    def get_current_selected_value(self, locator: Union[str, Locator]):
        element = self.get_element(locator)
        return element.input_value()

    @keyword('get list values')
    def get_list_values(self, locator: Union[str, Locator]):
        return self.get_element(locator).locator("xpath=./option").all_text_contents()

    @keyword('dropdown should be correct')
    def dropdown_should_be_correct(self, locator, item_list=None, state='enabled', default=None):
        element = self.get_element(locator)
        # Verify state
        if state == 'enabled':
            expect(element).to_be_enabled()
        elif state == 'disabled':
            expect(element).to_be_disabled()
        # Verify default value
        if default is not None:
            self.dropdown_current_value_should_be(element, default)
        # Verify item list
        if item_list is not None:
            self.dropdown_itemlist_should_be(element, item_list)

    @keyword('get item list length')
    def get_item_list_length(self, locator):
        return len(self.get_list_values(locator))
