from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest
import random
from .conftest import wait_for_load, wait_to_be_clickable, create_new_name, create_new_phone
from selenium.common.exceptions import NoSuchElementException


def test_login(driver):
    username_menu = driver.find_element(By.XPATH, "//div[starts-with(@class,'right-module-userNameWrap')]")
    assert username_menu.is_displayed()


def test_logout(driver):
    username_menu = driver.find_element(By.XPATH, "//div[starts-with(@class,'right-module-userNameWrap')]")
    username_menu.click()
    logout_button = driver.find_element(By.XPATH, "//a[@href = '/logout']")
    wait_to_be_clickable(driver, logout_button)
    logout_button.click()
    wait_for_load(driver)
    with pytest.raises(NoSuchElementException):
        username_menu = driver.find_element(By.XPATH, "//div[starts-with(@class,'right-module-userNameWrap')]")


def test_edit_contact_information(driver):
    new_name = create_new_name()
    new_phone = create_new_phone()
    driver.get("https://target.my.com/profile/contacts")
    wait_for_load(driver)
    fio_elem = driver.find_element(By.XPATH, "//div[@data-name = 'fio']")
    phone_elem = driver.find_element(By.XPATH, "//div[@data-name = 'phone']")
    fio_input = fio_elem.find_element(By.TAG_NAME, "input")
    phone_input = phone_elem.find_element(By.TAG_NAME, "input")
    previous_name = fio_input.get_attribute("value")
    previous_phone = phone_input.get_attribute("value")
    fio_input.clear()
    phone_input.clear()
    fio_input.send_keys(new_name)
    phone_input.send_keys(new_phone)
    save_button = driver.find_element(By.CLASS_NAME, "button_submit")
    save_button.click()
    driver.refresh()
    wait_for_load(driver)
    fio_elem = driver.find_element(By.XPATH, "//div[@data-name = 'fio']")
    phone_elem = driver.find_element(By.XPATH, "//div[@data-name = 'phone']")
    fio_input = fio_elem.find_element(By.TAG_NAME, "input")
    phone_input = phone_elem.find_element(By.TAG_NAME, "input")
    time.sleep(3)
    assert fio_input.get_attribute("value") != previous_name and \
           phone_input.get_attribute("value") != previous_phone


@pytest.mark.parametrize('locator, check_locator', [
        ((By.XPATH, "//a[@href='/segments']"),
         (By.XPATH, "//a[@href='/segments/segments_list']")),
        ((By.XPATH, "//a[@href='/statistics']"),
         (By.XPATH, "//a[@href='/statistics/summary']")),
    ])
def test_page_navigation(driver, locator, check_locator):
    button = driver.find_element(*locator)
    button.click()
    wait_for_load(driver)
    assert (driver.find_element(*check_locator))







