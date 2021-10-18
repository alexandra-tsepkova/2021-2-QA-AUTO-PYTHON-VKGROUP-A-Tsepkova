from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pytest
import time
import string
import random


TIMEOUT = 4

@pytest.fixture(scope='function', autouse=True)
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--lang=en_US')
#    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en_US'})
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
    log_button = driver.find_element(By.XPATH, "//div[starts-with(@class,'responseHead-module-button')]")
    log_button.click()
    email = driver.find_element(By.NAME, "email")
    password = driver.find_element(By.NAME, "password")
    email.send_keys("testingaccount@internet.ru")
    password.send_keys("ikYESaAr12a]")
    authform_button = driver.find_element(By.XPATH, "//div[starts-with(@class,'authForm-module-button')]")
    authform_button.click()
    wait_for_load(driver)
    yield driver


def wait_for_load(driver):
    try:
        WebDriverWait(driver, TIMEOUT
                      ).until(EC.presence_of_element_located((By.CLASS_NAME, "spinner")))

        WebDriverWait(driver, TIMEOUT
                      ).until_not(EC.presence_of_element_located((By.CLASS_NAME, "spinner")))

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