import allure
import pytest
from selenium.common.exceptions import NoSuchElementException

from base_test_case import BaseCase
from locators import dashboard_locators, page_locators, segment_locators
from settings import (campaign_name, segment_name_for_delete,
                      segment_name_for_input, url_for_campaign)


@allure.feature("Авторизация на сайте")
class TestAuthentication(BaseCase):
    @allure.title("Авторизация падает, если неправильный логин")
    @pytest.mark.UI
    def test_login_fails_wrong_password(self, page):
        page.login(wrong_psw=True)
        error_window = page.find(page_locators.ERROR_LOGIN)
        assert error_window.is_displayed()

    @allure.title("Авторизация падает, если данные неправильно отформатированы")
    @pytest.mark.UI
    def test_login_fails_invalid_input(self, page):
        page.login(invalid_log=True)
        error_window = page.find(page_locators.INVALID_LOGIN)
        assert error_window.is_displayed()


@allure.feature("Работа с кампаниями")
class TestCampaigns(BaseCase):
    @allure.title("Кампанию можно создать")
    @pytest.mark.UI
    def test_create_campaign(self, dashboard_page, path_to_pic):
        dashboard_page.create_campaign(path_to_pic, url_for_campaign, campaign_name)
        icon_success = dashboard_page.find(dashboard_locators.ICON_SUCCESS)
        assert icon_success.is_displayed()


@allure.feature("Работа с сегментами")
class TestSegments(BaseCase):
    @allure.title("Сегмент может быть создан")
    @pytest.mark.UI
    def test_create_segment(self, segment_page):
        segment_page.create_segment(segment_name_for_input)
        name = segment_page.find_complex_elem(
            segment_locators.SEGMENT_LIST_TABLE_NAME_COLUMN,
            segment_locators.segment_element(segment_name_for_input),
        )
        assert name

    @allure.title("Сегмент может быть удалён")
    @pytest.mark.UI
    def test_delete_segment(self, segment_page):
        segment_page.create_segment(segment_name_for_delete)
        segment_page.delete_segment(
            segment_locators.segment_element(segment_name_for_delete)
        )
        with pytest.raises(NoSuchElementException):
            segment_page.find(segment_locators.segment_element(segment_name_for_delete))
