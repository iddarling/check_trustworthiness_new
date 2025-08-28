import os
import csv
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from config import OUTPUT_TXT

class BaseTestCase:
    def __init__(self):
        self.driver = self.init_driver()

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def wait_for_element(self, by, value, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def write_result(self, bin_value, result):
        with open(OUTPUT_TXT, "a", encoding="utf-8") as f:
            f.write(f"БИН: {bin_value}, Статус: {result}\n")

    def quit(self):
        self.driver.quit()
