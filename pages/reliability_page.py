import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.selectors import Selectors

class ReliabilityPage:
    def __init__(self, driver):
        self.driver = driver
        # Кнопки и их уникальные лейблы
        self.buttons_and_labels = {
            "Enterprise": "Enterprise",
            "Finances": "Finances",
            "Purchases": "Purchases",
            "CEO": "CEO",
            "Founder": "Founder",
        }

    # Метод для выбора вкладки (по умолчанию Trustworthiness)
    def open_tab(self, tab_name="Trustworthiness"):
        wait = WebDriverWait(self.driver, 20)
        tab_xpath = Selectors.TAB_XPATH.format(tab_name)
        tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, tab_xpath))
        )
        tab.click()

    # Метод для выбора кнопки внутри вкладки
    def open_button(self, button_name):
        wait = WebDriverWait(self.driver, 20)
        button_xpath = Selectors.BUTTON_XPATH.format(button_name)
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        button.click()

    # Универсальный метод для получения статуса
    def get_status(self, label_text):
        xpath = Selectors.INFO_BLOCK_XPATH.format(label_text)
        try:
            element = WebDriverWait(self.driver, 30).until(
                lambda d: d.find_element(By.XPATH, xpath)
            )
            WebDriverWait(self.driver, 30).until(
                lambda d: element.text.strip() != ""
            )
            return element.text.strip()
        except:
            return "Нет данных"

    def get_status_with_retry(self, label_text, retries=3):
        for i in range(retries):
            status = self.get_status(label_text)
            if status and status != "Нет данных":
                return status
            time.sleep(3)
        return "Нет данных"

    def get_customs_status(self, label_text):
        return self.get_status_with_retry(label_text, retries=5)
