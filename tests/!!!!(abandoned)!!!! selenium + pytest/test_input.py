from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By

class TestGoogle:
    def test_chrome(self, chrome_driver):
        driver = chrome_driver
        driver.get("http://uitestingplayground.com/textinput")
        driver.find_element(By.ID, 'newButtonName').send_keys("basic text")


    def test_clear(self, chrome_driver):
        driver = chrome_driver
        driver.get("http://uitestingplayground.com/textinput")
        el = driver.find_element(By.ID, 'newButtonName')
        el.send_keys("basic text")
        el.clear()


    def test_copy_paste(self, chrome_driver):
        driver = chrome_driver
        driver.get("http://uitestingplayground.com/textinput")
        el = driver.find_element(By.ID, 'newButtonName')
        el.send_keys("basic text")

        action_chains = webdriver.ActionChains(driver)

        action_chains.key_down(Keys.CONTROL).send_keys("a").perform()
        action_chains.key_down(Keys.CONTROL).send_keys("c").perform()
        el.clear()
        el.click()
        action_chains.key_down(Keys.CONTROL).send_keys("v").perform()
