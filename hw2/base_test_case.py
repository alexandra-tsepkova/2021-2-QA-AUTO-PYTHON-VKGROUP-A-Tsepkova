import pytest
from _pytest.fixtures import FixtureRequest


class BaseCase:

    driver = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, request: FixtureRequest):
        self.driver = driver
