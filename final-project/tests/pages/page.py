from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from locators import basic_locators

CLICK_RETRY = 3
TIMEOUT = 5


class Page:
    def __init__(self, driver):
        self.driver = driver
        self.setup()

    def setup(self):
        pass

    def find(
        self,
        locator,
        visible=True,
        multiple=False,
        complex_elem=False,
        elem_to_search_in=None,
        timeout=TIMEOUT,
    ):
        element = None
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            if visible:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
        except TimeoutException:
            raise NoSuchElementException()
        if multiple:
            if not complex_elem:
                element = self.driver.find_elements(*locator)
            else:
                element = elem_to_search_in.find_elements(*locator)
        elif not multiple:
            if complex_elem:
                element = elem_to_search_in.find_element(*locator)
            else:
                element = self.driver.find_element(*locator)
        return element

    def click(self, locator, timeout=TIMEOUT):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator, timeout=timeout)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def login(self, login, password):
        username_window = self.find(basic_locators.USERNAME)
        password_window = self.find(basic_locators.PASSWORD)
        username_window.send_keys(login)
        password_window.send_keys(password)
        self.click(basic_locators.SUBMIT_BUTTON)

    def find_upper_menu(self):
        login_name_menu = self.find(basic_locators.LOGIN_NAME_MENU)
        vk_id = self.find(
            basic_locators.VK_ID_MENU,
            complex_elem=True,
            multiple=True,
            elem_to_search_in=login_name_menu,
        )
        return vk_id
