import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging.config
from os import path

logging.config.fileConfig(path.join(path.dirname(path.abspath(__file__)), 'logging.ini'))
GRID_URL = "http://26.172.242.18:4444"


@pytest.fixture
def chrome_driver():
    """Фикстура для Chrome через Grid"""
    options = Options()
    options.set_capability("browserName", "chrome")

    driver = webdriver.Remote(
        command_executor=GRID_URL,
        options=options
    )
    yield driver
    driver.quit()