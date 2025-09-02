from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, LOGIN, PASSWORD

from core.selectors import Selectors

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(BASE_URL)

    def login(self, username=LOGIN, password=PASSWORD):
        self.open()

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, Selectors.LOGIN_BUTTON))
        ).click()

        email = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, Selectors.EMAIL_INPUT))
        )
        password_input = self.driver.find_element(By.ID, Selectors.PASSWORD_INPUT)

        email.send_keys(username)
        password_input.send_keys(password)

        self.driver.find_element(By.XPATH, Selectors.SUBMIT_BUTTON).click()

        # ждём поле поиска как подтверждение входа
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, Selectors.SEARCH_INPUT))
        )
