import allure
import pytest
from client import ApiClient
from sqlclient import MysqlClient
import settings


@allure.feature("API authorization tests")
class TestApiAuthorization(ApiClient, MysqlClient):
    @allure.description(
        """Check that an existing user can log in using API request
            """
    )
    def test_login_existing_user(self, unauthorized_client):
        response = self.login(unauthorized_client, settings.login1, settings.password1)
        assert response.status_code == 200

    @allure.description(
        """Check that non-existing user can not log in using API request
                """
    )
    def test_login_non_existing_user(self, unauthorized_client):
        response = self.login(
            unauthorized_client, settings.normal_login(), settings.normal_password()
        )
        assert any((response.status_code == 404, response.status_code == 401))

    @allure.description(
        """Check that validation of username works on login API request
                """
    )
    def test_login_incorrect_format(self, unauthorized_client):
        response = self.login(
            unauthorized_client,
            settings.wrong_format_login(),
            settings.normal_password(),
        )
        assert response.text.find("Incorrect username length") >= 0

    @allure.description(
        """Check that authorized user can log out using API request
                    """
    )
    def test_logout(self, authorized_client):
        username = settings.login1
        self.go_to_main_page(authorized_client)
        self.check_database(username, "active", 1)
        self.logout(authorized_client)
        self.check_database(username, "active", 0)


@allure.feature("API registration tests")
class TestApiRegistration(ApiClient, MysqlClient):
    @allure.description(
        """Check that user can registrate with valid credentials using API
                    """
    )
    def test_register(self, unauthorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.normal_email(),
        )
        response = self.registrate_user(unauthorized_client, login, password, email)
        assert response.status_code == 200
        assert self.check_if_in_database(login)

    @allure.description(
        """Check that user can not registrate with invalid email credentials using API
                        """
    )
    def test_registration_incorrect_email_format(self, unauthorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.wrong_format_email(),
        )
        response = self.registrate_user(unauthorized_client, login, password, email)
        assert response.status_code == 400

    @allure.description(
        """Check that user can not registrate with invalid username credentials using API
                        """
    )
    def test_registration_incorrect_name_format(self, unauthorized_client):
        login, password, email = (
            settings.wrong_format_login(),
            settings.normal_password(),
            settings.normal_email,
        )
        response = self.registrate_user(unauthorized_client, login, password, email)
        assert response.status_code == 400

    @allure.description(
        """Check that newly registered user is on main page and active flag is set to 1 in database
                        """
    )
    def test_active_after_registration(self, unauthorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.normal_email(),
        )
        response = self.registrate_user(unauthorized_client, login, password, email)
        assert "Logged as" in response.text
        self.check_database(login, "active", 1)


@allure.feature("API requests tests")
class TestApiRequests(ApiClient, MysqlClient):
    @allure.description(
        """Check that new user with valid credentials can be added using special API request
                        """
    )
    def test_add_new_user(self, authorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.normal_email(),
        )
        response = self.add_user(authorized_client, login, password, email)
        assert response.status_code == 201

    @allure.description(
        """Check that already existing user can not be added again using special API request
                            """
    )
    def test_add_existing_user(self, authorized_client):
        response = self.add_user(
            authorized_client,
            settings.login1,
            settings.password1,
            settings.normal_email(),
        )
        assert response.status_code == 304

    @allure.description(
        """Check that user with invalid email credentials can not be added using special API request
                            """
    )
    def test_add_user_incorrect_email_format(self, authorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.wrong_format_email(),
        )
        response = self.add_user(authorized_client, login, password, email)
        assert response.status_code == 400

    @allure.description(
        """Check that user with invalid username credentials can not be added using special API request
                                """
    )
    def test_add_user_incorrect_name_format(self, authorized_client):
        login, password, email = (
            settings.wrong_format_login(),
            settings.normal_password(),
            settings.normal_email,
        )
        response = self.add_user(authorized_client, login, password, email)
        assert response.status_code == 400

    @allure.description(
        """Check that existing user can be blocked using special API request
                                """
    )
    def test_block_user(self, authorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.normal_email(),
        )
        self.add_user(authorized_client, login, password, email)
        response = self.block_user(authorized_client, login)
        assert response.status_code == 200
        self.check_database(login, "access", 0)

    @allure.description(
        """Check that non-existing user can not be blocked using special API request
                                    """
    )
    def test_block_non_existing_user(self, authorized_client):
        login = settings.normal_login()
        response = self.block_user(authorized_client, login)
        assert response.status_code == 404
        assert not self.check_if_in_database(login)

    @allure.description(
        """Check that blocked user is unauthorized
                                """
    )
    def test_blocked_user_unauthorize(self, authorized_client, unauthorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.normal_email(),
        )
        self.add_user(authorized_client, login, password, email)
        self.login(unauthorized_client, login, password)  # technically now authorized
        self.block_user(authorized_client, login)
        self.check_database(login, "access", 0)
        self.check_database(login, "active", 0)

    @allure.description(
        """Check that user can be accepted after being blocked
                                """
    )
    def test_accept_user(self, authorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.normal_email(),
        )
        self.add_user(authorized_client, login, password, email)
        self.block_user(authorized_client, login)
        self.check_database(login, "access", 0)
        response = self.accept_user(authorized_client, login)
        assert response.status_code == 200
        self.check_database(login, "access", 1)

    @allure.description(
        """Check that existing user can be deleted
                                """
    )
    def test_delete_user(self, authorized_client):
        login, password, email = (
            settings.normal_login(),
            settings.normal_password(),
            settings.normal_email(),
        )
        self.add_user(authorized_client, login, password, email)
        assert self.check_if_in_database(login)
        resp = self.delete_user(authorized_client, login)
        assert resp.status_code == 204
        assert not self.check_if_in_database(login)

    @allure.description(
        """Check that non-existing user can not be deleted
                                """
    )
    def test_delete_non_existing_user(self, authorized_client):
        login, password = settings.normal_login(), settings.normal_password()
        assert not self.check_if_in_database(login)
        resp = self.delete_user(authorized_client, login)
        assert resp.status_code == 404

    @allure.description(
        """Check that status of app can be correctly received
                                """
    )
    def test_check_status(self, unauthorized_client):
        response = self.check_status(unauthorized_client)
        assert response.status_code == 200
        assert response.text == '{"status":"ok"}\n'
