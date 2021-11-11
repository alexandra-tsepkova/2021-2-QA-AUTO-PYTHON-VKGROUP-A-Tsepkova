import pytest


class BaseCase:

    driver = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver):
        self.driver = driver
