import asyncio

import undetected_chromedriver as uc
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from Config import FILE_XPATH_BTN_ZOOM_REGISTRATION
from Contact.Contact import User


async def registration_user_zoom_link(user: User) -> bool:
    options = uc.ChromeOptions()
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--disable-notifications")
    # options.add_argument("--disable-popup-blocking")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-sync")
    # options.add_argument("--disable-web-security")
    # options.add_argument("--disable-default-apps")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-setuid-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-accelerated-2d-canvas")
    # options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    # options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--start-maximized')
    # options.add_argument('--disable-blink-features=AutomationControlled')

    # options.setExperimentalOption("useAutomationExtension", false)
    # options.setExperimentalOption("excludeSwitches",Collections.singletonList("enable-automation"))
    #
    # options.add_experimental_option("useAutomationExtension", False)
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #
    # options.add_argument(user_agent)
    # options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(
        executable_path='../chromedriver.exe',
        chrome_options=options
    )

    web_error = (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException)

    async def fill_form(contact: User):
        def fill_element(find_element='question_last_name', text=''):
            element = driver.find_element(value=find_element)
            element.clear()
            element.send_keys(text)

        await asyncio.sleep(1)
        fill_element('question_first_name', contact.first_name)
        await asyncio.sleep(0.5)
        fill_element('question_last_name', contact.last_name)
        await asyncio.sleep(0.5)
        fill_element('question_email', contact.email)
        await asyncio.sleep(0.5)

    driver.get(url=user.url_registration)
    await asyncio.sleep(1)
    # Accept Cookies and fill form
    for i in range(5):
        try:
            driver.find_element(value='onetrust-accept-btn-handler').click()
            await asyncio.sleep(0.5)
        except web_error:
            await asyncio.sleep(1)

    for i in range(5):
        driver.get(url=user.url_registration)
        try:
            await fill_form(user)
            await asyncio.sleep(1)
            print('fill_form_ok')

            try:
                with open(FILE_XPATH_BTN_ZOOM_REGISTRATION, mode='r', encoding='utf-8') as f:
                    xpath = f.read()
            except FileNotFoundError:
                xpath = '//div[@class="btn-register mgb-lg mgt-sm"]//button'

            driver.find_element(By.XPATH, xpath).click()
        except web_error:
            await asyncio.sleep(4)
            continue
        # check page is registration - ok
        await asyncio.sleep(1)
        try:
            driver.find_element(By.XPATH, xpath).click()
        except web_error:
            driver.close()
            driver.quit()
            await asyncio.sleep(1)
            return True

    driver.close()
    driver.quit()
    await asyncio.sleep(1)
    return False
