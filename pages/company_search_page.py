from selenium.webdriver.common.by import By
import time
from core.selectors import Selectors
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

class CompanySearchPage:
    def __init__(self, base):
        """Page object for search results. Accepts BaseTestCase to reuse robust actions."""
        self.base = base
        self.driver = base.driver

    def search(self, bin_value):
        """Search for a BIN/IIN and wait for a result (company or person)."""
        for attempt in range(3):
            try:
                # вводим БИН/ИИН
                self.base.safe_send_keys(By.XPATH, Selectors.SEARCH_INPUT, bin_value)
                time.sleep(0.5)
                # кликаем по кнопке поиска
                self.base.safe_click(By.XPATH, Selectors.FIND_BUTTON)
                time.sleep(0.5)
                # ждём появления либо ссылки на компанию, либо на физлицо
                try:
                    self.base.wait.until(lambda d: d.find_elements(By.XPATH, Selectors.COMPANY_PROFILE_LINK) or d.find_elements(By.XPATH, Selectors.PERSON_PROFILE_LINK))
                    return
                except TimeoutException:
                    # повторим цикл
                    raise
            except (StaleElementReferenceException, TimeoutException):
                print(f"🔁 DOM обновился, повторяем поиск ({attempt + 1}/3)...")
                time.sleep(1)

        raise Exception(f"❌ Не удалось выполнить поиск по БИН/ИИН: {bin_value}")

    def open_person_profile(self, retries=3, delay=0.5):
        """Open the first person profile from search results using a robust click.

        Retries a few times because the search results update dynamically and the
        element may appear or be replaced after initial load.
        """
        for attempt in range(retries):
            elem = self.base.wait_for_element(By.XPATH, Selectors.PERSON_PROFILE_LINK, timeout=5)
            if elem:
                if self.base.safe_click(By.XPATH, Selectors.PERSON_PROFILE_LINK):
                    # дождёмся вкладки благонадежность как признака загрузки профиля
                    self.base.wait_for_element(By.XPATH, Selectors.TAB_XPATH.format("Благонадежность"), timeout=10)
                    return True
            time.sleep(delay)
        return False
