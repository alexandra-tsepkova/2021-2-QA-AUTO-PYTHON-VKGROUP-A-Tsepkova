import pytest
from selenium.common.exceptions import NoSuchElementException

from base_test_case import BaseCase
from locators import dashboard_locators, page_locators, segment_locators
from settings import (
    campaign_name,
    segment_name_for_delete,
    segment_name_for_input,
    url_for_campaign,
)


class TestAuthentication(BaseCase):
    @pytest.mark.UI
    def test_login_fails_wrong_password(self, page):
        page.login(wrong_psw=True)
        error_window = page.find(page_locators.ERROR_LOGIN)
        assert error_window.is_displayed()

    @pytest.mark.UI
    def test_login_fails_invalid_input(self, page):
        page.login(invalid_log=True)
        error_window = page.find(page_locators.INVALID_LOGIN)
        assert error_window.is_displayed()


class TestCampaigns(BaseCase):
    @pytest.mark.UI
    def test_create_campaign(self, dashboard_page, path_to_pic):
        dashboard_page.click(dashboard_locators.CREATE_NEW_CAMPAIGN)
        dashboard_page.click(dashboard_locators.CAMPAIGN_AIM)
        input_url_window = dashboard_page.find(dashboard_locators.INPUT_URL)
        input_url_window.send_keys(url_for_campaign)
        input_name_window_class = dashboard_page.find(dashboard_locators.CAMPAIGN_NAME)
        dashboard_page.click(dashboard_locators.CLOSE_POPUP)
        dashboard_page.click(dashboard_locators.INPUT_NAME_WINDOW_CLEAR)
        input_name_window = input_name_window_class.find_element(
            *dashboard_locators.INPUT_CAMPAIGN_NAME
        )
        input_name_window.click()
        input_name_window.send_keys(campaign_name)

        elements = self.driver.find_elements(*dashboard_locators.LOAD_PIC_FIELD)
        elements[1].send_keys(path_to_pic)

        dashboard_page.click(dashboard_locators.SUBMIT_BANNER_BUTTON)
        dashboard_page.click(dashboard_locators.SAVE_CAMPAIGN)
        icon_success = dashboard_page.find(dashboard_locators.ICON_SUCCESS)
        assert icon_success.is_displayed()


class TestSegments(BaseCase):
    @staticmethod
    def create_segment(segment_page, segment_name):
        try:
            segment_page.click(segment_locators.CREATE_NEW_SEGMENT)
        except NoSuchElementException:
            try:
                segment_page.click(segment_locators.SUBMIT_BUTTON)
            except NoSuchElementException:
                raise
        segment_page.click(segment_locators.CHECKBOX)
        segment_page.click(segment_locators.CREATE_SEGMENT_BUTTON)
        segment_name_class = segment_page.find(segment_locators.SEGMENT_NAME_CLASS)
        segment_name_input = segment_name_class.find_element(
            *segment_locators.SEGMENT_NAME_INPUT
        )
        segment_name_input.clear()
        segment_name_input.send_keys(segment_name)
        segment_page.click(segment_locators.SUBMIT_BUTTON)

    @pytest.mark.UI
    def test_create_segment(self, segment_page):
        self.create_segment(segment_page, segment_name_for_input)
        name_column = segment_page.find(segment_locators.SEGMENT_LIST_TABLE_NAME_COLUMN)
        name = name_column.find_element(*segment_locators.SEGMENT_LIST_CREATED_SEGMENT)
        assert name

    @pytest.mark.UI
    def test_delete_segment(self, segment_page):
        self.create_segment(segment_page, segment_name_for_delete)
        segment_to_delete = segment_page.find(
            segment_locators.SEGMENT_ELEMENT_TO_DELETE
        )
        segment_id = segment_to_delete.get_attribute("href").split("/")[-1]

        try:
            scroll_handler = segment_page.find(segment_locators.SCROLL_HANDLER)
            segment_page.action_chains.click_and_hold(scroll_handler).move_by_offset(
                100, 0
            ).release().perform()
        except NoSuchElementException:
            pass

        segment_page.click(segment_locators.segment_delete_cross(segment_id))
        segment_page.click(segment_locators.CONFIRM_REMOVE)
        segment_page.wait_for_load()
        with pytest.raises(NoSuchElementException):
            segment_page.find(segment_locators.SEGMENT_ELEMENT_TO_DELETE)
