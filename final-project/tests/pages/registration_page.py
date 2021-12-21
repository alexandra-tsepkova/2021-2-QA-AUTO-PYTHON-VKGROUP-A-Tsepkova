from pages.page import Page
from locators import basic_locators


class RegistrationPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click(basic_locators.REGISTRATION_BUTTON)

    def register(self, username, password, email):
        email_window = self.find(basic_locators.EMAIL)
        username_window = self.find(basic_locators.USERNAME)
        password_window = self.find(basic_locators.PASSWORD)
        confirm_window = self.find(basic_locators.CONFIRM_PASSWORD)
        username_window.send_keys(username)
        password_window.send_keys(password)
        email_window.send_keys(email)
        confirm_window.send_keys(password)
        self.click(basic_locators.CHECKBOX)
        self.click(basic_locators.SUBMIT_BUTTON)


