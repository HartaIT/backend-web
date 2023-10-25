import json
import os
import re
import time
from datetime import datetime, timedelta

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

path = "../files/KeywordList.json"
file = open(path)
keywords = json.load(file)

path = "../files/Cities.json"
file = open(path)
cities_array = json.load(file)



class PostItem:
    def __init__(self):
        self.Keywords = []
        self.City = []
        self.Logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Facebook_icon.svg/640px-Facebook_icon.svg.png'

    Company: int = None
    DatePosted: str = None
    Text: str = None
    Link: str = None
    Keywords = []
    City = []


def main_func():
    global driver
    driver = webdriver_setup.get_driver(False, False, False)

    driver.implicitly_wait(2)
    driver.set_page_load_timeout(8)
    start_scraping()


def start_scraping():
    if webdriver_setup.facebook_login(driver):

        all_companies = supabase.table('Companies').select('*').execute().data

        for company in all_companies:
            for link in company['Links']:
                if link.__contains__('facebook'):
                    try:
                        scrape_page(company, link)
                    except:
                        print(f"couldn't scrape facebook for company {company['Name']} | {company['id']}")


def scrape_page(company, facebook_link):
    driver.get(facebook_link)

    driver.execute_script("window.scrollTo(0,2500)")
    time.sleep(2)

    posts = []
    try:
        posts = driver.find_elements(By.XPATH,
                                     '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div')
    except:
        print(f"couldn't get posts list {facebook_link}")

    for post in posts:
        post_item = PostItem()
        post_item.Company = company['id']
        post_item.Link = facebook_link

        try:
            date = post.find_element(By.XPATH, './div[2]/div/div[2]/div/div[2]/span/span/span[2]').text
            if date[0].isdigit():
                date = (datetime.today() - timedelta(days=int(date[0]))).date()
            else:
                if not date.__contains__(','):
                    words = date.split()
                    date = words[0] + ' ' + words[1]
                    date = date + ', ' + str(datetime.today().year)

                date = datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")

            post_item.DatePosted = date
        except:
            print(f"couldn't get time for a post {facebook_link}")

        try:
            text_elem = post.find_element(By.XPATH, './div[3]/div[1]/div/div')

            try:
                driver.implicitly_wait(0.1)
                text_elem.find_element(By.XPATH, "//*[contains(text(), 'See more')]").click()
            except:
                pass

            driver.implicitly_wait(0.5)

            text = text_elem.find_element(By.XPATH, '//div[@data-ad-preview="message"]').text

            post_item.Text = text

            text = unidecode(text.lower())
            text = text.replace('bucharest', 'bucuresti')

            for keyword in keywords:
                if text.__contains__(keyword['to_find']):
                    post_item.Keywords.append(keyword['to_put'])

            for city in cities_array:
                if re.search(rf"\b{city}\b", text) is not None:
                    post_item.City.append(city['name'])
        except:
            print(f"couldn't get text for a post {facebook_link}")

        if len(post_item.City) < 1:
            post_item.City = company['City']

        if len(post_item.Keywords) > 0:
            try:
                post_item.City = list(set(post_item.City))
                post_item.Keywords = list(set(post_item.Keywords))
                supabase.table('Posts').insert(post_item.__dict__).execute()
            except:
                print(f"conflict for company {facebook_link}")


main_func()
