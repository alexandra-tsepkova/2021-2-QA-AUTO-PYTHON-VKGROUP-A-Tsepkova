import allure
import pytest
import requests
import settings


class ApiClient:
    username = None
    password = None
    session = None

    @pytest.fixture()
    def unauthorized_client(self):
        session = requests.Session()
        yield session
        session.close()

    @pytest.fixture()
    def authorized_client(self, login=settings.login1, password=settings.password1):
        session = requests.Session()
        self.login(session, login, password)
        yield session
        session.close()

    @staticmethod
    def login(session, login, password):
        url_to_request = f"http://{settings.myapp}/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"username": f"{login}", "password": f"{password}", "submit": "Login"}
        with allure.step(
            f"sending POST request to log in user {login} with password {password}"
        ):
            res = session.post(url_to_request, headers=headers, data=data)
        with allure.step(f"request status code {res.status_code}"):
            pass
        return res

    @staticmethod
    def add_user(session, login, password, email):
        url_to_request = f"http://{settings.myapp}/api/add_user"
        headers = {"Content-Type": "application/json"}
        data = {"username": f"{login}", "password": f"{password}", "email": f"{email}"}
        with allure.step(
            f"sending POST request to add user {login} with password {password} and email {email}"
        ):
            res = session.post(url_to_request, headers=headers, json=data)
        return res

    @staticmethod
    @allure.step("go to main page")
    def go_to_main_page(session):
        url_to_request = f"http://{settings.myapp}/welcome"
        res = session.get(url_to_request)
        allure.step(
            f"sending get request to go to main page; status code {res.status_code}"
        )
        return res

    @staticmethod
    def logout(session):
        url_to_request = f"http://{settings.myapp}/logout"
        res = session.get(url_to_request)
        allure.step(f"sending get request to log out; status code {res.status_code}")
        return res

    @staticmethod
    def block_user(session, username):
        url_to_request = f"http://{settings.myapp}/api/block_user/{username}"
        res = session.get(url_to_request)
        allure.step(f"sending get request block a user; status code {res.status_code}")
        return res

    @staticmethod
    def accept_user(session, username):
        url_to_request = f"http://{settings.myapp}/api/accept_user/{username}"
        res = session.get(url_to_request)
        return res

    @staticmethod
    def delete_user(session, username):
        url_to_request = f"http://{settings.myapp}/api/del_user/{username}"
        res = session.get(url_to_request)
        allure.step(
            f"sending get request to delete user; status code {res.status_code}"
        )
        return res

    @staticmethod
    def registrate_user(session, login, password, email):
        url_to_request = f"http://{settings.myapp}/reg"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": f"{login}",
            "email": f"{email}",
            "password": f"{password}",
            "confirm": f"{password}",
            "term": "y",
            "submit": "Register",
        }
        res = session.post(url_to_request, headers=headers, data=data)
        allure.step(
            f"sending post request to registrate user {login} with password {password} and email {email}, status code {res.status_code}"
        )
        return res

    @staticmethod
    def check_status(session):
        url_to_request = f"http://{settings.myapp}/status"
        res = session.get(url_to_request)
        allure.step(
            f"sending get request to check status; status code {res.status_code}"
        )
        return res
