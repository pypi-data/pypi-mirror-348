from typing import Union

from playwright.sync_api import expect, Locator
from robotlibcore import keyword
from .base_context import BaseContext



class TableHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword('Table column should have')
    def table_column_should_have(self, locator: Union[str, Locator], *items):
        """
        Check for table header contains some labels or not

        *locator*: the locator of the table

        *items*: list of strings
        """
        element = self.get_element(locator)
        for item in items:
            expect(element.locator(f'//th[contains(.,"{item}")]')).to_be_visible()

    @keyword('Table row should have')
    def table_row_should_have(self, locator: Union[str, Locator], row_index: int, *items):
        """
        Check for table row contains some labels or not

        *row_index*: index of row starting from 1

        *locator*: the locator of the table

        *items*: list of strings
        """
        element = self.get_element(locator)
        for item in items:
            expect(element.locator(f'//tr[{row_index}][contains(.,"{item}")]')).to_be_visible()


    @keyword('Table cell value should be')
    def table_cell_value_should_be(self, locator: Union[str, Locator], row_key: str,
                                   column_name: str, expected_cell_value: str):
        """
        Check for specific cell in a table that has expected value

        *row_key*: unique string in the row that can tell which row we are looking for

        *locator*: the locator of the table

        *column_name*: Name of the column

        *expected_cell_value*: The expected value in the target cell
        """
        element = self.get_element(locator)
        col_title_pos = element.locator(f'//th[text()="{column_name}"]/preceding-sibling::*').count() + 1
        expect(element.locator(f'//tr[.//*[text()="{row_key}"]][.//td[position()={col_title_pos} '
                                 f'and text()="{expected_cell_value}"]]')).to_be_visible()
