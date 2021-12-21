import allure
import pytest
import settings
from base_case_ui import BaseCase
from locators import basic_locators
from sqlclient import MysqlClient


@allure.feature("UI authorization tests")
class TestUiLogin(BaseCase, MysqlClient):
    @allure.description(
        """Check that existing user can log in
                                    """
    )
    def test_login_existing_user(self, page):
        login, password = settings.login1, settings.password1
        page.login(login, password)
        self.check_database(login, "active", 1)
        assert page.find(basic_locators.LOGOUT_BUTTON)

    @allure.description(
        """Check that non-existing user can not be logged in
                                    """
    )
    def test_login_non_existing_user(self, page):
        login, password = settings.login1, settings.normal_password()
        page.login(login, password)
        window = page.find(basic_locators.WARNING_WINDOW)
        assert window.text == "Invalid username or password"

    @allure.description(
        """Check that login page correctly validates login
                                    """
    )
    def test_wrong_format_login(self, page):
        login, password = settings.wrong_format_login(), settings.normal_password()
        page.login(login, password)
        window = page.find(basic_locators.WARNING_WINDOW)
        assert window.text == "Incorrect username length"

    @allure.description(
        """Check that authorized user can be logged out
                                    """
    )
    def test_logout(self, welcome_page):
        welcome_page.click(basic_locators.LOGOUT_BUTTON)
        self.check_database(welcome_page.username, "active", 0)
        assert welcome_page.find(basic_locators.USERNAME)


@allure.feature("UI registration tests")
class TestUiRegister(BaseCase, MysqlClient):
    @allure.description(
        """Check that user with valid credentials can be registrated
                                    """
    )
    def test_registration_normal_user(self, registration_page):
        login, password = settings.normal_login(), settings.normal_password()
        email = settings.normal_email()
        registration_page.register(login, password, email)
        assert self.check_if_in_database(login)

    @pytest.mark.skip("Repetitive")
    def test_active_after_registration(self, registration_page):
        login, password = settings.normal_login(), settings.normal_password()
        email = settings.normal_email()
        registration_page.register(login, password, email)
        assert registration_page.find(basic_locators.LOGOUT_BUTTON)
        self.check_database(login, "active", 1)

    @allure.description(
        """Check that user with invalid login can not be registrated
                                    """
    )
    def test_register_wrong_form_login(self, registration_page):
        login, password = settings.wrong_format_login(), settings.normal_password()
        email = settings.normal_email()
        registration_page.register(login, password, email)
        window = registration_page.find(basic_locators.WARNING_WINDOW)
        assert window.text == "Incorrect username length"
        assert not self.check_if_in_database(login)

    @allure.description(
        """Check that user with invalid email can not be registrated
                                    """
    )
    def test_register_wrong_form_email(self, registration_page):
        login, password = settings.normal_login(), settings.normal_password()
        email = settings.wrong_format_email()
        registration_page.register(login, password, email)
        window = registration_page.find(basic_locators.WARNING_WINDOW)
        assert window.text == "Invalid email address"
        assert not self.check_if_in_database(login)


@allure.feature("UI main page tests")
class TestUiMainPage(BaseCase, MysqlClient):
    @allure.description(
        """Check that buttons have correct links
                                    """
    )
    @pytest.mark.parametrize("keyword", ["HOME", "Python"])
    def test_check_correct_link_button(self, welcome_page, keyword):
        button = welcome_page.buttons[keyword]
        button.click()
        if keyword == "HOME":
            assert welcome_page.driver.current_url == "http://myapp:8080/welcome/"
        else:
            assert "python" in welcome_page.driver.current_url

    @allure.description(
        """Check that dropdown menu links are opened in new tab
                                    """
    )
    @pytest.mark.parametrize(
        "keyword, inner_button_keyword",
        [
            ("Python", "history"),
            ("Python", "flask"),
            ("Linux", "centos7"),
            ("Network", "news"),
            ("Network", "download"),
            ("Network", "examples"),
        ],
    )
    def test_check_dropdown_menu_links_open_new_tab(
        self, welcome_page, keyword, inner_button_keyword
    ):
        upper_button = welcome_page.find_upper_button(keyword)
        welcome_page.get_button_from_dropdown_menu(
            upper_button, inner_button_keyword
        ).click()
        assert len(self.driver.window_handles) == 2

    @allure.description(
        """Check that dropdown menu links are correct
                                    """
    )
    @pytest.mark.parametrize(
        "keyword, inner_button_keyword",
        [
            ("Python", "history"),
            ("Python", "flask"),
            ("Linux", "centos7"),
            ("Network", "news"),
            ("Network", "download"),
            ("Network", "examples"),
        ],
    )
    def test_check_dropdown_menu_links_have_correct_hrefs(
        self, welcome_page, keyword, inner_button_keyword
    ):
        upper_button = welcome_page.find_upper_button(keyword)
        button = welcome_page.get_button_from_dropdown_menu(
            upper_button, inner_button_keyword
        )
        assert inner_button_keyword in button.get_attribute("href").lower()

    @allure.description(
        """Check that central button links are correct
                                    """
    )
    @pytest.mark.parametrize(
        "keyword, href_keyword",
        [("api", "application"), ("future", "future"), ("smtp", "smtp")],
    )
    def test_check_central_links_have_correct_hrefs(
        self, welcome_page, keyword, href_keyword
    ):
        button = welcome_page.find_central_button(keyword)
        assert href_keyword in button.get_attribute("href").lower()

    @allure.description(
        """Check that central button links open in new tab
                                    """
    )
    @pytest.mark.parametrize("keyword", ["api", "future", "smtp"])
    def test_check_central_links_open_new_tab(self, welcome_page, keyword):
        welcome_page.find_central_button(keyword).click()
        assert len(self.driver.window_handles) == 2

    @allure.description(
        """Check that new users do not have vk id
                                    """
    )
    def test_new_users_no_vk_id(self, registration_page):
        login, password = settings.normal_login(), settings.normal_password()
        email = settings.normal_email()
        registration_page.register(login, password, email)
        vk_id = registration_page.find_upper_menu()[1]
        assert len(vk_id.text) == 0

    @allure.description(
        """Check that admin has vk id 1
                                    """
    )
    def test_admin_has_vk_id(self, welcome_page):
        vk_id = welcome_page.find_upper_menu()[1]
        assert "VK ID: 1" in vk_id.text

    @allure.description(
        """Check that the quote on main page is still there
                                    """
    )
    def test_quote_on_main_page(self, welcome_page):
        lower_menu = welcome_page.find(basic_locators.LOWER_MENU)
        quote_menus = welcome_page.find(
            basic_locators.QUOTE_MENU,
            multiple=True,
            complex_elem=True,
            elem_to_search_in=lower_menu,
        )
        assert quote_menus[0].text == "powered by ТЕХНОАТОМ"
        assert len(quote_menus[1].text) > 0

    @allure.description(
        """Check that right upper menu has info about user such as "Logged as..."
                                    """
    )
    def test_info_about_user(self, welcome_page):
        info_menu = welcome_page.find_upper_menu()[0]
        assert welcome_page.username in info_menu.text
