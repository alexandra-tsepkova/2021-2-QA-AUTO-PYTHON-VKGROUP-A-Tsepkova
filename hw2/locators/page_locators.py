from selenium.webdriver.common.by import By

SPINNER = (By.CLASS_NAME, "spinner")
AUTHFORM_BUTTON = (By.XPATH, "//div[starts-with(@class,'authForm-module-button')]")
LOG_BUTTON = (By.XPATH, "//div[starts-with(@class,'responseHead-module-button')]")
LOGIN_EMAIL = (By.NAME, "email")
LOGIN_PASSWORD = (By.NAME, "password")
ERROR_LOGIN = (By.CLASS_NAME, "formMsg_text")
INVALID_LOGIN = (By.XPATH, "//div[starts-with(@class, 'notify-module-content')]")
