import time

from pages.page import Page
import settings
from locators import basic_locators
from selenium.webdriver import ActionChains


class WelcomePage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = settings.login1
        self.password = settings.password1
        self.buttons = {}
        self.login(self.username, self.password)
        self.assign_upper_buttons()

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def assign_upper_buttons(self):
        buttons = self.find(basic_locators.UPPER_BUTTON, multiple=True)
        for b in buttons:
            self.buttons[b.text] = b
        self.buttons["HOME"] = self.find(basic_locators.HOME_BUTTON)

    def find_upper_button(self, name):
        buttons = self.find(basic_locators.UPPER_BUTTON, multiple=True)
        for b in buttons:
            if b.text == name:
                return b

        return None

    def get_button_from_dropdown_menu(self, button, keyword):
        self.action_chains.move_to_element(button).perform()
        dropdown_menu = self.find(basic_locators.DROPDOWN_MENU_OPEN)
        inner_buttons = self.find(
            basic_locators.DROPDOWN_MENU_BUTTON,
            multiple=True,
            complex_elem=True,
            elem_to_search_in=dropdown_menu,
        )

        for b in inner_buttons:
            if keyword in b.text.lower():
                self.action_chains.move_to_element(b).perform()
                return b

    def find_central_button(self, keyword):
        central_elem = self.find(basic_locators.CENTRAL_ELEMENT, multiple=True)
        for e in central_elem:
            text = self.find(
                basic_locators.CENTRAL_TEXT, complex_elem=True, elem_to_search_in=e
            )
            href = self.find(
                basic_locators.CENTRAL_BUTTON, complex_elem=True, elem_to_search_in=e
            )
            if keyword in text.text.lower():
                return href
