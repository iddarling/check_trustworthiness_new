class Selectors:
    SEARCH_INPUT = "//input[@type='search']"
    FIND_BUTTON = "//span[normalize-space()='Find']"
    LOGIN_BUTTON = "(//span[@class='hidden text-sm font-semibold text-white dark:text-gray-900 lg:inline-block min-w-[44px]'])[1]"
    EMAIL_INPUT = "Enter email"
    PASSWORD_INPUT = "Enter password"
    SUBMIT_BUTTON = "//button[@type='submit']"
    COMPANY_PROFILE_LINK = "//a[contains(@href, '/company/')]"

    # ReliabilityPage selectors
    TAB_XPATH = "//span[normalize-space()='{}']"
    BUTTON_XPATH = "//button[.//span[text()='{}']]"
    INFO_BLOCK_XPATH = (
        "//div[contains(@id, 'infoBlock-') and "
        ".//*[contains(normalize-space(), '{}')]]"
        "//*[self::div or self::span][normalize-space()][last()]"
    )
