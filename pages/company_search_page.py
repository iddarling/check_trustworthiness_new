from selenium.webdriver.common.by import By
import time

class CompanySearchPage:
    def __init__(self, driver):
        self.driver = driver

    def search(self, bin_value):
        search_input = self.driver.find_element(By.XPATH, "//input[@type='search']")
        search_input.clear()
        search_input.send_keys(bin_value)
        self.driver.find_element(By.XPATH, "//span[normalize-space()='Find']").click()
        time.sleep(2)
