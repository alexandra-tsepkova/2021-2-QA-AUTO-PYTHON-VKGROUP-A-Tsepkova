from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators import page_locators
from settings import invalid_login, login, passw, wrong_passw

CLICK_RETRY = 3
TIMEOUT = 5


class Page:
    def __init__(self, driver):
        self.driver = driver
        self.setup()

    def setup(self):
        pass

    def wait_for_load(self):
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located(page_locators.SPINNER)
            )

            WebDriverWait(self.driver, TIMEOUT).until_not(
                EC.presence_of_element_located(page_locators.SPINNER)
            )

        except TimeoutException:
            pass

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def find(self, locator, visible=True, timeout=TIMEOUT):
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
        element = self.driver.find_element(*locator)
        return element

    def click(self, locator, timeout=TIMEOUT):
        for i in range(CLICK_RETRY):
            try:
                self.wait_for_load()
                elem = self.find(locator, timeout=timeout)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def login(self, wrong_psw=False, invalid_log=False):
        login_string = invalid_login if invalid_log else login
        password_string = wrong_passw if wrong_psw else passw

        self.click(page_locators.LOG_BUTTON)

        email_window = self.find(page_locators.LOGIN_EMAIL)
        password_window = self.find(page_locators.LOGIN_PASSWORD)
        email_window.send_keys(login_string)
        password_window.send_keys(password_string)

        self.click(page_locators.AUTHFORM_BUTTON)

    def find_complex_elem(self, class_locator, elem_locator, is_input=False):
        elem_class = self.find(class_locator)
        elem = elem_class.find_element(*elem_locator)
        if is_input:
            elem.clear()
        return elem

    def scroll_right(self, scroll_handler_locator):
        try:
            scroll_handler = self.find(scroll_handler_locator)
            self.action_chains.click_and_hold(scroll_handler).move_by_offset(
                100, 0
            ).release().perform()
        except NoSuchElementException:
            pass
