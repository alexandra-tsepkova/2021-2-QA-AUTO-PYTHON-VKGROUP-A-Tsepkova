import pytest
from .locators import basic_locators

from .conftest import (create_new_name, create_new_phone, wait_for_load,
                       wait_to_be_clickable, check_elem_not_found)


def test_login(driver):
    username_menu = driver.find_element(*basic_locators.USERNAME_MENU)
    assert username_menu.is_displayed()


def test_logout(driver):
    username_menu = driver.find_element(*basic_locators.USERNAME_MENU)
    username_menu.click()
    logout_button = driver.find_element(*basic_locators.LOGOUT_BUTTON)
    wait_to_be_clickable(driver, logout_button)
    logout_button.click()
    wait_for_load(driver)
    check_elem_not_found(driver, basic_locators.USERNAME_MENU)


def test_edit_contact_information(driver):
    new_name = create_new_name()
    new_phone = create_new_phone()
    driver.get("https://target.my.com/profile/contacts")
    wait_for_load(driver)
    fio_elem = driver.find_element(*basic_locators.FIO_ELEM)
    phone_elem = driver.find_element(*basic_locators.PHONE_ELEM)
    fio_input = fio_elem.find_element(*basic_locators.INPUT_WINDOW)
    phone_input = phone_elem.find_element(*basic_locators.INPUT_WINDOW)
    previous_name = fio_input.get_attribute("value")
    previous_phone = phone_input.get_attribute("value")
    fio_input.clear()
    fio_input.send_keys(new_name)
    phone_input.clear()
    phone_input.send_keys(new_phone)
    save_button = driver.find_element(*basic_locators.SAVE_BUTTON)
    save_button.click()
    driver.refresh()
    wait_for_load(driver)
    fio_elem = driver.find_element(*basic_locators.FIO_ELEM)
    phone_elem = driver.find_element(*basic_locators.PHONE_ELEM)
    fio_input = fio_elem.find_element(*basic_locators.INPUT_WINDOW)
    phone_input = phone_elem.find_element(*basic_locators.INPUT_WINDOW)
    assert fio_input.get_attribute("value") != previous_name
    assert phone_input.get_attribute("value") != previous_phone


@pytest.mark.parametrize('locator, check_locator', [
        (basic_locators.SEGMENT_BUTTON,
         basic_locators.SEGMENTS_LIST),
        (basic_locators.STATISTICS_BUTTON,
         basic_locators.STATISTICS_SUMMARY),
    ])
def test_page_navigation(driver, locator, check_locator):
    button = driver.find_element(*locator)
    button.click()
    wait_for_load(driver)
    assert (driver.find_element(*check_locator))
