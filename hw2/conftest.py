import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
    chrome = webdriver.Chrome(ChromeDriverManager().install())
    chrome.get("https:target.my.com/")
    yield chrome
    chrome.quit()


@pytest.fixture(scope="session")
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def path_to_pic(repo_root):
    return os.path.join(repo_root, pic_name)
