class Selectors:
    SEARCH_INPUT = "//input[@id='Введите ИИН, БИН, ФИО, название компании']"
    FIND_BUTTON = "//span[normalize-space()='Найти']"
    LOGIN_BUTTON = "(//span[@class='hidden text-sm font-semibold text-white dark:text-gray-900 lg:inline-block min-w-[44px]'])[1]"
    EMAIL_INPUT = "Введите email"
    PASSWORD_INPUT = "Введите пароль"
    SUBMIT_BUTTON = "//button[@type='submit']"
    # избегаем ссылки на linkedin
    COMPANY_PROFILE_LINK = "//a[contains(@href, '/company/') and not(contains(@href, 'linkedin.com'))]"

    # ReliabilityPage selectors
    TAB_XPATH = "//span[normalize-space()='{}']"
    BUTTON_XPATH = "//button[.//span[text()='{}']]"
    INFO_BLOCK_XPATH = (
        "//div[contains(@id, 'infoBlock-') and "
        ".//*[contains(normalize-space(), '{}')]]"
        "//*[self::div or self::span][normalize-space()][last()]"
    )
