from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, LOGIN, PASSWORD

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(BASE_URL)

    def login(self, username=LOGIN, password=PASSWORD):
        self.open()

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,
                "(//span[@class='hidden text-sm font-semibold text-white dark:text-gray-900 lg:inline-block min-w-[44px]'])[1]"))
        ).click()

        email = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "Enter email"))
        )
        password_input = self.driver.find_element(By.ID, "Enter password")

        email.send_keys(username)
        password_input.send_keys(password)

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # ждём поле поиска как подтверждение входа
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
        )
