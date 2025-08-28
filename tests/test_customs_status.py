import time
from core.base_case import BaseTestCase
from pages.login_page import LoginPage
from pages.company_search_page import CompanySearchPage
from pages.reliability_page import ReliabilityPage
from config import BIN_FILE, BASE_URL
import os

BIN_FILE = os.path.join(os.path.dirname(__file__), "bin_list.txt")

def test_check_customs_status():
    case = BaseTestCase()
    try:
        login_page = LoginPage(case.driver)
        search_page = CompanySearchPage(case.driver)
        reliability_page = ReliabilityPage(case.driver)

        # авторизация
        login_page.login()

        # Список кнопок с соответствующими label_text
        buttons_and_labels = [
            ("Enterprise", 'In the list of "Comprehensive Outgoing Customs Inspections for the 2nd half of 2025 year"'),
            # ("Finances", "In the list of taxpayers whose transactions were made without actual performance of work, provision of services, or shipment of goods"),
            # ("Purchases", "In the list of TOP 100 suppliers of state purchases"),
            # ("CEO", "Tax and Customs Payment Debt"),
            # ("Founder", "In the list of legal entities with offshore participation"),
        ]

        if not os.path.exists(BIN_FILE):
            raise FileNotFoundError(f"Файл BIN-лист не найден: {BIN_FILE}")

            # Читаем BIN-лист
        with open(BIN_FILE, "r") as f:
            bin_list = [line.strip() for line in f if line.strip()]

        for bin_value in bin_list:
            print(f"\n🔎 Проверка БИН: {bin_value}")
            search_page.search(bin_value)

            # открыть профиль компании
            case.driver.find_element("xpath", "//a[contains(@href, '/company/')]").click()

            # Сначала открываем вкладку Trustworthiness
            reliability_page.open_tab("Trustworthiness")

            # Проходим по кнопкам внутри вкладки
            for button_name, label_text in buttons_and_labels:
                reliability_page.open_button(button_name)
                status = reliability_page.get_customs_status(label_text)
                print(f"{button_name} → {status}")
                case.write_result(f"{bin_value} - {button_name}", status)

            # возвращаемся на главную
            case.driver.get(BASE_URL)
            time.sleep(2)
    finally:
        case.quit()


