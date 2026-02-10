import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from core.selectors import Selectors


class CompanySearchPage:
    def __init__(self, base):
        self.base = base
        self.driver = base.driver
        self.wait = base.wait

    def search(self, bin_value: str, retries: int = 6) -> str | None:
        for attempt in range(1, retries + 1):
            try:
                inp = self.wait.until(EC.element_to_be_clickable((By.XPATH, Selectors.SEARCH_INPUT)))
                inp.click()
                inp.clear()
                inp.send_keys(bin_value)

                try:
                    self.base.safe_click(By.XPATH, Selectors.FIND_BUTTON)
                except Exception:
                    inp.send_keys(Keys.ENTER)

                def got_result(d):
                    if d.find_elements(By.XPATH, Selectors.COMPANY_PROFILE_LINK):
                        return "company"
                    if d.find_elements(By.XPATH, Selectors.PERSON_PROFILE_LINK):
                        return "person"
                    return False

                return self.wait.until(got_result)

            except (StaleElementReferenceException, TimeoutException):
                print(f"🔁 DOM обновился/таймаут, повторяем поиск ({attempt}/{retries})...")
                time.sleep(0.8)

        return None

    def open_person_profile(self, retries: int = 3, delay: float = 0.6) -> bool:
        """
        Открывает первый профиль физлица из результатов.
        Возвращает True если открылся профиль, иначе False.
        """
        for attempt in range(1, retries + 1):
            try:
                link = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, Selectors.PERSON_PROFILE_LINK))
                )
                link.click()

                # признак что профиль реально открылся
                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, Selectors.TAB_XPATH.format("Благонадежность")))
                )
                return True

            except (StaleElementReferenceException, TimeoutException):
                print(f"🔁 Не удалось открыть профиль физлица ({attempt}/{retries})...")
                time.sleep(delay)

        return False
