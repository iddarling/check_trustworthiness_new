import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.base_case import BaseTestCase
from pages.login_page import LoginPage
from pages.company_search_page import CompanySearchPage
from pages.reliability_page import ReliabilityPage
from core.selectors import Selectors
from config import BASE_URL, BIN_FILE,OUTPUT_TXT


def test_check_customs_status():
    case = BaseTestCase()
    print("CWD:", os.getcwd())
    print("OUTPUT_TXT:", OUTPUT_TXT)

    try:
        driver = case.driver
        wait = WebDriverWait(driver, 12)

        login_page = LoginPage(driver)
        search_page = CompanySearchPage(case)
        reliability_page = ReliabilityPage(driver)

        # авторизация
        login_page.login()
        time.sleep(1.5)

        buttons_and_labels = [
            ("Предприятие", "Профилактический контроль и надзор на 1-ое полугодие 2026 года"),
            # ("Финансы", "..."),
            # ("Закупки", "..."),
            # ("Руководитель", "..."),
            # ("Учредитель", "..."),
        ]

        if not os.path.exists(BIN_FILE):
            raise FileNotFoundError(f"Файл BIN-лист не найден: {BIN_FILE}")

        with open(BIN_FILE, "r", encoding="utf-8") as f:
            bin_list = [line.strip() for line in f if line.strip()]

        for bin_value in bin_list:
            print(f"\n🔎 Проверка БИН: {bin_value}")
            time.sleep(0.5)

            # 1) ПОИСК: search() должен вернуть "company" / "person" / None
            result_type = search_page.search(bin_value)
            time.sleep(0.5)
            # 2) НИЧЕГО НЕ НАШЛОСЬ — мягко логируем и идём дальше
            if result_type is None:
                status = "Не найдено/поиск не выполнен (нет результатов или нестабильный DOM)"
                print(status)
                for button_name, _ in buttons_and_labels:
                    case.write_result(f"{bin_value} - {button_name}", status)

                driver.get(BASE_URL)
                time.sleep(0.8)
                continue
            time.sleep(0.5)

            # 3) НАЙДЕНА КОМПАНИЯ — открываем профиль компании
            if result_type == "company":
                try:
                    link = wait.until(EC.element_to_be_clickable((By.XPATH, Selectors.COMPANY_PROFILE_LINK)))
                    link.click()
                except Exception as e:
                    status = f"Найдено, но не удалось открыть профиль компании: {type(e).__name__}"
                    print(status)
                    for button_name, _ in buttons_and_labels:
                        case.write_result(f"{bin_value} - {button_name}", status)

                    driver.get(BASE_URL)
                    time.sleep(0.8)
                    continue

            # 4) НАЙДЕНО ФИЗЛИЦО — открываем профиль физлица (если используешь этот путь)
            elif result_type == "person":
                opened = search_page.open_person_profile()
                if not opened:
                    status = "Найдено физлицо, но профиль не открылся"
                    print(status)
                    for button_name, _ in buttons_and_labels:
                        case.write_result(f"{bin_value} - {button_name}", status)

                    driver.get(BASE_URL)
                    time.sleep(0.8)
                    continue

            else:
                # на случай неожиданных значений
                status = f"Неизвестный тип результата поиска: {result_type}"
                print(status)
                for button_name, _ in buttons_and_labels:
                    case.write_result(f"{bin_value} - {button_name}", status)

                driver.get(BASE_URL)
                time.sleep(0.8)
                continue

            # 5) Если профиль открылся — работаем с благонадежностью
            reliability_page.open_tab("Благонадежность")
            time.sleep(2)

            for button_name, label_text in buttons_and_labels:
                reliability_page.open_button(button_name)
                status = reliability_page.get_customs_status(label_text)
                print(f"{button_name} → {status}")
                case.write_result(f"{bin_value} - {button_name}", status)

            # 6) Возвращаемся на базовую страницу перед следующим БИН
            driver.get(BASE_URL)
            time.sleep(0.8)

    finally:
        case.quit()
