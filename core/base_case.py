import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)
from webdriver_manager.chrome import ChromeDriverManager

from config import OUTPUT_TXT

class BaseTestCase:
    def __init__(self):
        self.driver = self.init_driver()
        self.wait = WebDriverWait(self.driver, 20)
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # --- устойчивое ожидание элемента ---
    def wait_for_element(self, by, value, timeout=20):
        """Ожидание появления элемента в DOM"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logging.error(f"⏰ Не найден элемент за {timeout} сек: {by}={value}")
            return None

    # --- устойчивый клик ---
    def safe_click(self, by, value, retries=3, delay=1):
        """Robust click with retries and fallbacks.

        Tries the normal click, then JS click, then ActionChains if necessary.
        Returns True on success, False otherwise.
        """
        from selenium.common.exceptions import ElementNotInteractableException, WebDriverException
        from selenium.webdriver.common.action_chains import ActionChains

        for attempt in range(retries):
            try:
                elem = self.wait_for_element(by, value)
                if elem:
                    self.wait.until(EC.element_to_be_clickable((by, value)))
                    try:
                        elem.click()
                        return True
                    except (ElementNotInteractableException, WebDriverException):
                        # try JS click
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                            self.driver.execute_script("arguments[0].click();", elem)
                            return True
                        except Exception:
                            # ActionChains as last resort
                            try:
                                ActionChains(self.driver).move_to_element(elem).click().perform()
                                return True
                            except Exception as e:
                                logging.warning(f"🔁 Click fallback failed on attempt {attempt+1}: {e}")
                time.sleep(delay)
            except (StaleElementReferenceException, NoSuchElementException) as e:
                logging.warning(f"🔁 DOM обновился (попытка {attempt+1}/{retries}): {e}")
                time.sleep(delay)
        logging.error(f"❌ Не удалось кликнуть по элементу: {value}")
        return False

    # --- безопасный ввод ---
    def safe_send_keys(self, by, value, text, retries=3):
        for attempt in range(retries):
            try:
                elem = self.wait_for_element(by, value)
                if elem:
                    elem.clear()
                    elem.send_keys(text)
                    return True
            except (StaleElementReferenceException, NoSuchElementException):
                logging.warning(f"🔁 Элемент обновился, повтор ввода ({attempt+1}/{retries})")
                time.sleep(1)
        logging.error(f"❌ Не удалось ввести текст в {value}")
        return False

    # --- запись результатов ---
    def write_result(self, bin_value, result):
        out_path = OUTPUT_TXT

        # если OUTPUT_TXT без директории — пишем в текущую рабочую папку
        out_dir = os.path.dirname(out_path)
        if not out_dir:
            out_dir = os.getcwd()
            out_path = os.path.join(out_dir, os.path.basename(out_path))

        os.makedirs(out_dir, exist_ok=True)

        # 🔎 отладка: куда реально пишем
        logging.info(f"📝 Запись результата в файл: {out_path}")

        with open(out_path, "a", encoding="utf-8") as f:
            f.write(f"БИН: {bin_value}, Статус: {result}\n")
            f.flush()
            os.fsync(f.fileno())


    def quit(self):
        self.driver.quit()
