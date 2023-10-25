import json
import os
import re
import time

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from unidecode import unidecode

from Utils import webdriver_setup

load_dotenv()

from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

path = "../files/Cities.json"
file = open(path)
cities_array = json.load(file)

driver: webdriver_setup.webdriver.Chrome


def main_func():
    global driver
    driver = webdriver_setup.get_driver(False, False, False)

    get_links()


def get_links():
    all_companies = supabase.table('Companies').select('*').execute().data

    for company in all_companies:
        found = False

        link = company['Links'][0]
        driver.get(link)

        try:
            driver.find_element(By.CLASS_NAME, 'modal__dismiss').click()
            time.sleep(0.25)
        except:
            pass

        driver.execute_script("window.scrollTo(0,1500)")

        try:
            driver.find_element(By.CLASS_NAME, 'show-more-less__button').click()
            time.sleep(0.5)
        except:
            pass

        locations = driver.find_elements(By.CSS_SELECTOR, '.show-more-less__list li.mb-3 div')

        for location in locations:
            location = location.text
            location = unidecode(location.lower())
            location = location.replace('bucharest', 'bucuresti')
            location = location.replace('bucarest', 'bucuresti')

            for city in cities_array:
                if (re.search(rf"\b{city}\b", location) is not None) and (
                        company['City'] is None or not company['City'].__contains__(city['name'])):
                    found = True

                    if company['City'] is None:
                        company['City'] = []
                    company['City'].append(city['name'])

                    supabase.table('Companies').update({'City': company['City']}).eq('id', company['id']).execute()

        if not found and company['City'] is None:
            print(f"didn't find city for company {company['Name']}")


main_func()
