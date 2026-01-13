import time
from core.base_case import BaseTestCase
from pages.login_page import LoginPage
from pages.company_search_page import CompanySearchPage
from pages.person_reliability_page import PersonReliabilityPage
from core.selectors import Selectors
from config import BIN_FILE, BASE_URL
import os
from selenium.webdriver.common.by import By


BIN_FILE = os.path.join(os.path.dirname(__file__), "iin_list.txt")

def test_check_person_status():
    case = BaseTestCase()
    try:
        login_page = LoginPage(case)
        search_page = CompanySearchPage(case)
        reliability_page = PersonReliabilityPage(case)

        # авторизация
        login_page.login()
        # login() waits for the search input; no fixed sleep needed

        # список проверок физлиц
        checks = [
            "В списке лиц, причастных к террористической деятельности",
            # "В списке лиц, совершивших насильственные действия сексуального характера в отношении несовершеннолетних",
            # "В перечне организаций и лиц, связанных с финансированием терроризма и экстремизма",
            # "В списке исключенных из перечня организаций и лиц, связанных с финансированием терроризма и экстремизма",
            # "В розыске без вести пропавших лиц",
            # "В розыске преступников",
            # "В розыске должников/ответчиков по исполнительным документам",
            # "В списке должников по алиментам",
            # "Арест на банковские счета",
            # "Арест на имущество",
            # "Временное ограничение на выезд из РК",
            # "Реализация арестованного имущества",
            # "Запрет на регистрационные действия",
            # "Запрет на совершение нотариальных действий",
            # "Арест на транспорт",
            # "В реестре торгов арестованного имущества",
            # "Должник по исполнительным производствам",
            # "Должник, временно ограниченный на выезд из Республики Казахстан",
            # "Задолженность по налогам и таможенным платежам",
            # "Участие в судебных делах",
            # "Проблема в компаниях с таким руководителем",
            # "Объявление о возбуждении производства по делу о реабилитации и порядке заявления требований кредиторами",
            # "Объявление о проведении собрания кредиторов при реабилитационной процедуре",
            # "Объявления о возбуждении дела о банкротстве и порядке заявления требовании кредиторами временному управляющему",
            # "Объявление о признании банкротом и ликвидации с возбуждением процедуры банкротства",
            # "Объявление о проведении собрания кредиторов в процедуре банкротства",
            # "Объявления о применении в отношении должника процедуры реструктуризации задолженности",
            # "В перечне участников процедур по восстановлению платежеспособности и процедур банкротства граждан в судебном и внесудебном порядке",
        ]       

        if not os.path.exists(BIN_FILE):
            raise FileNotFoundError(f"Файл ИИН-лист не найден: {BIN_FILE}")

        with open(BIN_FILE, "r") as f:
            iin_list = [line.strip() for line in f if line.strip()]

        for iin in iin_list:
            print(f"\n🔎 Проверка ИИН: {iin}")
            search_page.search(iin)
            # search() waits for either company or person result
            time.sleep(0.5)
            # открыть профиль физлица
            if not search_page.open_person_profile():
                print("⚠️ Профиль физлица не найден, пропускаем")
                case.write_result(f"{iin}", "Профиль не найден")
                case.driver.get(BASE_URL)
                case.wait_for_element(By.XPATH, Selectors.SEARCH_INPUT, timeout=3)
                continue
            reliability_page.open_tab("Благонадежность")
            # open_tab waits for the tab to be clickable and clicks it
            for label in checks:
                status = reliability_page.get_status_retry(label)
                print(f"{label} → {status}")
                case.write_result(f"{iin} - {label}", status)

            case.driver.get(BASE_URL)
            case.wait_for_element(By.XPATH, Selectors.SEARCH_INPUT, timeout=3)
    finally:
        case.quit()
