from selenium.webdriver.common.by import By
import time
from core.selectors import Selectors

class CompanySearchPage:
    def __init__(self, driver):
        self.driver = driver

    def search(self, bin_value):
        search_input = self.driver.find_element(By.XPATH, Selectors.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(bin_value)
        self.driver.find_element(By.XPATH, Selectors.FIND_BUTTON).click()
        time.sleep(2)
