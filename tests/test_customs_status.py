import time
from core.base_case import BaseTestCase
from pages.login_page import LoginPage
from pages.company_search_page import CompanySearchPage
from pages.reliability_page import ReliabilityPage
from core.selectors import Selectors
from config import BIN_FILE, BASE_URL
import os

BIN_FILE = os.path.join(os.path.dirname(__file__), "bin_list.txt")

def test_check_customs_status():
    case = BaseTestCase()
    try:
        login_page = LoginPage(case.driver)
        search_page = CompanySearchPage(case)
        reliability_page = ReliabilityPage(case.driver)

        # авторизация
        login_page.login()
        time.sleep(2)
        buttons_and_labels = [
            #("Предприятие", 'В списке индивидуальных предпринимателей и юридических лиц, в отношении которых вступило в законную силу определение суда о прекращении реабилитационной процедуры'),
            ("Финансы", "В реестре лиц, получающих средства или иное имущество из-за рубежа, подлежащем публикации за 2-ое полугодие 2025 года"),
            # ("Закупки", "Ненадежный участник государственных закупок РК"),
            # ("Руководитель", "Долг по налогам и таможенным платежам"),
            # ("Учредитель", "В списке юридических лиц с офшорным участием"),
        ]

        if not os.path.exists(BIN_FILE):
            raise FileNotFoundError(f"Файл BIN-лист не найден: {BIN_FILE}")

        with open(BIN_FILE, "r") as f:
            bin_list = [line.strip() for line in f if line.strip()]

        for bin_value in bin_list:
            print(f"\n🔎 Проверка БИН: {bin_value}")
            search_page.search(bin_value)
            time.sleep(0.5)
            # открыть профиль компании через селектор
            case.driver.find_element("xpath", Selectors.COMPANY_PROFILE_LINK).click()

            reliability_page.open_tab("Благонадежность")
            time.sleep(5)
            for button_name, label_text in buttons_and_labels:
                reliability_page.open_button(button_name)
                status = reliability_page.get_customs_status(label_text)
                print(f"{button_name} → {status}")
                case.write_result(f"{bin_value} - {button_name}", status)

            case.driver.get(BASE_URL)
            time.sleep(2)
    finally:
        case.quit()


