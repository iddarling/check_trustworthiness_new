from selenium.webdriver.common.by import By
import time
from core.selectors import Selectors
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

class CompanySearchPage:
    def __init__(self, base):
        self.base = base
        self.driver = base.driver
    time.sleep(0.5)
    def search(self, bin_value):
        """Поиск компании по БИН с защитой от stale"""
        for attempt in range(3):
            try:
                # вводим БИН
                self.base.safe_send_keys(By.XPATH, Selectors.SEARCH_INPUT, bin_value)
                time.sleep(0.5)
                # кликаем по кнопке поиска
                self.base.safe_click(By.XPATH, Selectors.FIND_BUTTON)
                time.sleep(0.5)
                # ждём, пока появится результат
                self.base.wait_for_element(By.XPATH, Selectors.COMPANY_PROFILE_LINK)
                return
            except (StaleElementReferenceException, TimeoutException):
                print(f"🔁 DOM обновился, повторяем поиск ({attempt + 1}/3)...")
                time.sleep(1)

        raise Exception(f"❌ Не удалось выполнить поиск по БИН: {bin_value}")
