from selenium.webdriver.common.by import By

USERNAME = (By.ID, "username")
PASSWORD = (By.ID, "password")
EMAIL = (By.ID, "email")
CONFIRM_PASSWORD = (By.ID, "confirm")
SUBMIT_BUTTON = (By.ID, "submit")
LOGOUT_BUTTON = (By.ID, "logout")
WARNING_WINDOW = (By.ID, "flash")
REGISTRATION_BUTTON = (By.XPATH, "//a[@href = '/reg']")
CHECKBOX = (By.ID, "term")

HOME_BUTTON = (By.XPATH, "//a[@href = '/']")
UPPER_BUTTON = (By.CLASS_NAME, "uk-parent")
DROPDOWN_MENU = (By.CLASS_NAME, "uk-dropdown")
DROPDOWN_MENU_BUTTON = (By.TAG_NAME, "a")
DROPDOWN_MENU_OPEN = (By.CLASS_NAME, "uk-open")

CENTRAL_ELEMENT = (By.CLASS_NAME, "uk-width-1-3")
CENTRAL_BUTTON = (By.TAG_NAME, "a")
CENTRAL_TEXT = (By.CLASS_NAME, "uk-text-middle")

LOGIN_NAME_MENU = (By.ID, "login-name")
VK_ID_MENU = (By.TAG_NAME, "li")

LOWER_MENU = (By.CLASS_NAME, "uk-text-large")
QUOTE_MENU = (By.TAG_NAME, "p")
