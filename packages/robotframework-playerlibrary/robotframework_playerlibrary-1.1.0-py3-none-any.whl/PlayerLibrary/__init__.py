from robotlibcore import DynamicCore
from .browser_handler import BrowserHandler
from .api_handler import APIHandler
from .button_handler import ButtonHandler
from .checkbox_handler import CheckboxHandler
from .datepicker_handler import DatePickerHandler
from .dropdown_handler import DropdownHandler
from .element_handler import ElementHandler
from .iframe_handler import IframeHandler
from .page_handler import PageHandler
from .table_handler import TableHandler
from .textbox_handler import TextboxHandler


class PlayerLibrary(DynamicCore):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self,
                 assertion_timeout: int = 10000):
        self.assertion_timeout = assertion_timeout
        libraries = [APIHandler(self), BrowserHandler(self), ButtonHandler(self), CheckboxHandler(self),
                     DatePickerHandler(self), DropdownHandler(self), ElementHandler(self), IframeHandler(self), PageHandler(self),
                     TableHandler(self), TextboxHandler(self)]
        DynamicCore.__init__(self, libraries)
