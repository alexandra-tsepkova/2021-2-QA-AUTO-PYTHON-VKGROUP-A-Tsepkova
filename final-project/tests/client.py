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
        url_to_request = "http://0.0.0.0:8081/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": f"{login}",
            "password": f"{password}",
            "submit": "Login"
        }
        res = session.post(url_to_request, headers=headers, data=data)
        return res

    @staticmethod
    def add_user(session, login, password, email):
        url_to_request = "http://0.0.0.0:8081/api/add_user"
        headers = {"Content-Type": "application/json"}
        data = {
            "username": f"{login}",
            "password": f"{password}",
            "email": f"{email}"
        }
        res = session.post(url_to_request, headers=headers, json=data)
        return res

    @staticmethod
    def go_to_main_page(session):
        url_to_request = "http://0.0.0.0:8081/welcome"
        res = session.get(url_to_request)
        return res

    @staticmethod
    def logout(session):
        url_to_request = "http://0.0.0.0:8081/logout"
        res = session.get(url_to_request)
        return res

    @staticmethod
    def block_user(session, username):
        url_to_request = f"http://0.0.0.0:8081/api/block_user/{username}"
        res = session.get(url_to_request)
        return res

    @staticmethod
    def accept_user(session, username):
        url_to_request = f"http://0.0.0.0:8081/api/accept_user/{username}"
        res = session.get(url_to_request)
        return res

    @staticmethod
    def delete_user(session, username):
        url_to_request = f"http://0.0.0.0:8081/api/del_user/{username}"
        res = session.get(url_to_request)
        return res

    @staticmethod
    def registrate_user(session, login, password, email):
        url_to_request = "http://0.0.0.0:8081/reg"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": f"{login}",
            "email": f"{email}",
            "password": f"{password}",
            "confirm": f"{password}",
            "term": "y",
            "submit": "Register"
        }
        res = session.post(url_to_request, headers=headers, data=data)
        return res

    @staticmethod
    def check_status(session):
        url_to_request = "http://0.0.0.0:8081/status"
        res = session.get(url_to_request)
        return res
