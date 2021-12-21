import os
import shutil
import sys

import pytest
from selenium import webdriver
from pages.welcome_page import WelcomePage
from pages.page import Page
from pages.registration_page import RegistrationPage


@pytest.fixture
def page(driver):
    return Page(driver=driver)


@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver=driver)


@pytest.fixture
def welcome_page(driver):
    return WelcomePage(driver=driver)


@pytest.fixture
def driver():
    capabilities = {
        "browserName": "chrome",
        "version": "95.0",
        "enableVNC": True,
        "enableVideo": False,
        "selenoid:options": {
            "applicationContainers": ["final-project_myapp_1"],
        },
    }

    chrome = webdriver.Remote(
        "http://selenoid:4444/wd/hub", desired_capabilities=capabilities
    )
    chrome.get("http://myapp:8080/")
    yield chrome
    chrome.quit()


@pytest.fixture(scope="session")
def base_temp_dir():
    if sys.platform.startswith("win"):
        base_dir = "C:\\tests"
    else:
        base_dir = "/tmp/tests"

    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    os.makedirs(base_dir)
    return base_dir


@pytest.fixture(scope="function")
def temp_dir(base_temp_dir, request):
    test_dir = os.path.join(
        base_temp_dir, request._pyfuncitem.nodeid.replace("/", "_").replace(":", "_")
    )
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope="session")
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))
