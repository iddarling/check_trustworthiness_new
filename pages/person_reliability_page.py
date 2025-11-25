import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.selectors import Selectors

class PersonReliabilityPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)

    def open_tab(self, tab_name="Благонадежность"):
        wait = WebDriverWait(self.driver, 50)
        tab_xpath = Selectors.TAB_XPATH.format(tab_name)
        tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, tab_xpath))
        )
        tab.click()
        
    def get_status(self, label_text):
        """
        Получает статус по тексту лейбла, например:
        "В списке лиц, причастных к террористической деятельности"
        """
        xpath = Selectors.INFO_BLOCK_XPATH.format(label_text)
        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text.strip()
        except:
            return "Нет данных"

    def get_status_retry(self, label_text, retries=3):
        """Повторная попытка на случай медленной загрузки"""
        for i in range(retries):
            status = self.get_status(label_text)
            if status and status != "Нет данных":
                return status
            time.sleep(1)
        return "Нет данных"
    