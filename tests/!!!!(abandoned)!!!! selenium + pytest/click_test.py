from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

class TestClick:
    def test_click(self, chrome_driver):
        driver = chrome_driver
        driver.get("http://uitestingplayground.com/click")
        driver.find_element(By.ID, 'badButton').click()
        for _ in range(2):
            driver.find_element(By.ID, 'badButton').click()
            break
        pass