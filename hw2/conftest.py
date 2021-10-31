import os
import random
import string

import pytest
from selenium import webdriver

from pages.dashboard_page import DashboardPage
from pages.page import Page
from pages.segment_page import SegmentPage
from settings import pic_name

TIMEOUT = 4


@pytest.fixture
def page(driver):
    return Page(driver=driver)


@pytest.fixture
def dashboard_page(driver):
    return DashboardPage(driver=driver)


@pytest.fixture
def segment_page(driver):
    return SegmentPage(driver=driver)


@pytest.fixture
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--lang=en_US")
    chrome = webdriver.Chrome(
        chrome_options=chrome_options,
        executable_path="/home/alexandra/drivers/chromedriver",
    )
    chrome.get("https:target.my.com/")
    yield chrome
    chrome.quit()


def create_new_name():
    output_string = "".join(
        random.SystemRandom().choice(string.ascii_letters) for _ in range(10)
    )
    return output_string


def create_new_phone():
    output_string = "".join(
        random.SystemRandom().choice(string.digits) for _ in range(10)
    )
    return output_string


@pytest.fixture(scope="session")
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def path_to_pic(repo_root):
    return os.path.join(repo_root, pic_name)
