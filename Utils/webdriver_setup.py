import json
import random

from selenium.webdriver.common.by import By
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")


def set_proxy():
    global wire_options

    # path = "ccrawler\\files\\Proxies.json"
    # file = open(path)
    # proxies_array = json.load(file)
    #
    # proxy = random.choice(proxies_array)
    # wire_options = {
    #     'proxy': {
    #         'http': f"socks5://{proxy['user']}:{proxy['pass']}@{proxy['ip']}:{proxy['port']}",
    #         'verify_ssl': False,
    #     },
    #     'disable_capture': True
    # }


def set_user_agent():
    global options

    # path = "ccrawler\\files\\UserAgents.json"
    # file = open(path)
    # agents_array = json.load(file)
    #
    # agent = random.choice(agents_array)
    # options.add_argument(f"--user-agent={agent['agent']}")


def set_headless():
    global options
    options.add_argument('--headless')


def get_driver(with_proxy: bool, with_user_agent: bool, with_headless: bool):
    global options

    if with_proxy:
        set_proxy()
    if with_user_agent:
        set_user_agent()
    if with_headless:
        set_headless()

    driver = webdriver.Chrome(options=options)

    return driver


def linkedin_login(driver):
    script_template = '''
                    const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
                    await sleep(500)
                    document.getElementById('username').value="R_email"
                    await sleep(500)
                    document.getElementById('password').value="R_password"
                    await sleep(1000)
                    document.getElementsByClassName('btn__primary--large from__button--floating')[0].click()
                    await sleep(500)
                '''

    path = "../files/LinkedInAccounts.json"
    file = open(path)
    accounts_array = json.load(file)

    for account in accounts_array:
        try:
            driver.get('https://www.linkedin.com/login')

            script = script_template
            script = script.replace("R_email", account['email'])
            script = script.replace("R_password", account['password'])

            driver.execute_script(script)
            elem = driver.find_element(By.CLASS_NAME,
                                       'global-nav')

            if not (elem is None):
                return True

        except:
            print("this account didn't work, trying next...")

    return False


def facebook_login(driver):
    driver.get("https://www.facebook.com")

    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        buttons[12].click()
    except:
        print('no cookies?')

    path = "../files/FacebookAccounts.json"
    file = open(path)
    accounts_array = json.load(file)

    script_template = f'''
                        const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
                        await sleep(500)
                        document.getElementById('email').value="{accounts_array[0]['email']}"
                        await sleep(500)
                        document.getElementById('pass').value="{accounts_array[0]['password']}"
                        await sleep(500)
                        document.getElementsByName('login')[0].click()
                        await sleep(1000)
                    '''

    try:
        driver.execute_script(script_template)

        elem = driver.find_element(By.CSS_SELECTOR, "[aria-label='Home']")
        if elem is not None:
            return True
    except:
        print("couldn't login to facebook")

    return False


def linkedin_logout(driver):
    driver.get('https://www.linkedin.com/m/logout')
    return True
