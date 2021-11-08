import random
import string

from .locators import basic_locators
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .settings import (
    login_string,
    password_string
)

TIMEOUT = 4


@pytest.fixture(scope='function', autouse=True)
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--lang=en_US')
    chrome = webdriver.Chrome(
        chrome_options=chrome_options,
        executable_path="/home/alexandra/drivers/chromedriver",
    )
    chrome.get("https:target.my.com/")
    yield chrome
    chrome.quit()


@pytest.fixture(scope='function', autouse=True)
def login(driver):
    wait_for_load(driver)
    log_button = driver.find_element(*basic_locators.LOG_BUTTON)
    log_button.click()
    email = driver.find_element(*basic_locators.EMAIL_INPUT)
    password = driver.find_element(*basic_locators.PASSWORD_INPUT)
    email.send_keys(login_string)
    password.send_keys(password_string)
    authform_button = driver.find_element(*basic_locators.AUTHFORM_BUTTON)
    authform_button.click()
    wait_for_load(driver)
    yield driver


def wait_for_load(driver):
    try:
        WebDriverWait(driver, TIMEOUT
                      ).until(EC.presence_of_element_located(basic_locators.SPINNER))

        WebDriverWait(driver, TIMEOUT
                      ).until_not(EC.presence_of_element_located(basic_locators.SPINNER))

    except TimeoutException:
        pass


def wait_to_be_clickable(driver, element):
    try:
        WebDriverWait(driver, TIMEOUT
                      ).until(EC.element_to_be_clickable(element))
    except TimeoutException:
        pass


def create_new_name():
    output_string = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(10))
    return output_string


def create_new_phone():
    output_string = ''.join(random.SystemRandom().choice(string.digits) for _ in range(10))
    return output_string


def check_elem_not_found(driver, locator):
    with pytest.raises(NoSuchElementException):
        driver.find_element(*locator)
