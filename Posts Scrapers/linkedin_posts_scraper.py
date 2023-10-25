import json
import os
import time
import re
from unidecode import unidecode
from datetime import datetime, timedelta
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from Utils import webdriver_setup

driver = webdriver_setup.get_driver(False, True, False)

from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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

    Company: int = None
    DatePosted: str = None
    Text: str = None
    Link: str = None
    Logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/1200px-LinkedIn_icon.svg.png'
    Keywords = []
    City = []


def main_func():
    if webdriver_setup.linkedin_login(driver):
        webdriver_setup.linkedin_logout(driver)
        time.sleep(5)

        driver.implicitly_wait(5)
        driver.set_page_load_timeout(10)
        start_scraping()


def start_scraping():
    all_companies = supabase.table('Companies').select('*').execute().data

    for company in all_companies:
        for link in company['Links']:
            if link.__contains__('linkedin'):
                try:
                    scrape_page(company, link)
                except:
                    print(f"couldn't scrape facebook for company {company['Name']} | {company['id']}")


def scrape_page(company, linkedin_url):
    driver.get(linkedin_url)

    driver.execute_script("window.scrollTo(0,2500)")
    time.sleep(2)

    posts_list = []
    try:
        posts_list = driver.find_elements(By.CSS_SELECTOR, '.updates__list li.mb-1')
    except:
        print(f"couldn't get posts for company {linkedin_url}")

    for post in posts_list:
        post_item = PostItem()
        post_item.Company = company['id']
        post_item.Link = linkedin_url

        driver.execute_script("arguments[0].scrollIntoView();", post)

        try:
            date = post.find_element(By.CSS_SELECTOR, 'time').text

            nr = int(date[0])
            days = 0

            if date[1] == 'd':
                days = nr
            if date[1] == 'w':
                days = nr * 7
            if date[1] == 'm':
                days = nr * 28

            date_posted = (datetime.today() - timedelta(days=days)).date()

            post_item.DatePosted = date_posted.strftime("%Y-%m-%d")
        except:
            print(f"couldn't get time for a post {linkedin_url}")

        try:
            text = post.find_element(By.CSS_SELECTOR, 'p.attributed-text-segment-list__content').text
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
            print(f"couldn't get text for a post {linkedin_url}")

        if len(post_item.City) < 1:
            post_item.City = company['City']

        if len(post_item.Keywords) > 0:
            try:
                post_item.City = list(set(post_item.City))
                post_item.Keywords = list(set(post_item.Keywords))
                supabase.table('Posts').insert(post_item.__dict__).execute()
            except:
                print(f"conflict for company {linkedin_url}")


main_func()
