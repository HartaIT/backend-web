import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from unidecode import unidecode

from Utils import webdriver_setup

load_dotenv()

from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

driver: webdriver_setup.webdriver.Chrome


def main_func():
    global driver
    driver = webdriver_setup.get_driver(False, False, False)
    if webdriver_setup.linkedin_login(driver):
        start_scraping()


class CompanyItem:
    Name: str = None
    Logo: str = None
    Category: str = None
    Links: str = [None]

    def to_unicode(self):
        self.Name = unidecode(self.Name)
        self.Category = unidecode(self.Category)


def start_scraping():
    page = 0
    while page <= 100:
        base_url = 'https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B"106670623"%5D&industryCompanyVertical=%5B"96"%2C"4"%2C"1855"%2C"3"%2C"3099"%2C"3100"%2C"3101"%2C"3102"%2C"3103"%2C"3104"%2C"3105"%2C"3106"%2C"3107"%2C"3130"%5D&origin=FACETED_SEARCH&page=0&sid=Oec'
        page += 1

        index1 = base_url.rfind('page=') + 5
        index2 = base_url.find('&sid')
        new_url = base_url[:index1] + str(page) + base_url[index2:]

        try:
            driver.get(new_url)
            elem = driver.find_element(By.CLASS_NAME,
                                       'entity-result__primary-subtitle')

            if not (elem is None):
                parse_page()

        except:
            print('error')


def parse_page():
    companies = driver.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')

    for company in companies:
        company_item = CompanyItem()

        subtitle = company.find_element(By.CSS_SELECTOR, '.entity-result__primary-subtitle').text
        splice_index = subtitle.find('•')
        category = subtitle[:splice_index - 1]

        company_item.Name = company.find_element(By.CSS_SELECTOR, '.entity-result__title-text .app-aware-link').text
        company_item.Logo = company.find_element(By.CSS_SELECTOR,
                                                 '.entity-result__universal-image img').get_attribute('src')
        company_item.Category = category
        company_item.Links = [company.find_element(By.CSS_SELECTOR,
                                                   '.entity-result__title-text .app-aware-link').get_attribute('href')]

        company_item.to_unicode()
        supabase.table('Companies').insert(company_item.__dict__).execute()

main_func()
