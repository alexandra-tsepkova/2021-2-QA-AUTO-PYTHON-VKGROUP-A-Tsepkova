from settings import login_string, password_string


class BaseData:
    login_headers = {
            "Referer": "https://target.my.com/",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    login_data = {
        "email": login_string,
        "password": password_string,
        "continue": "https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
        "failure": "https://account.my.com/login/",
    }
