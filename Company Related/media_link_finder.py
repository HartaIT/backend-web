import os

from dotenv import load_dotenv
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

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
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(10)
    driver.get("https://www.google.com")
    driver.find_elements(By.TAG_NAME, "button")[3].click()

    start_searching()


def start_searching():
    all_companies = supabase.table('Companies').select('*').execute().data

    # remove progress bar
    total_companies = len(all_companies)
    companies_done = 0

    for company in all_companies:
        no_fb_link = True
        no_ig_link = True

        # remove later
        def rem_link(temp_link):
            if (temp_link is None or temp_link.__contains__('/photo') or temp_link.__contains__(
                    '/post') or temp_link.__contains__('/video') or temp_link.__contains__(
                '/hashtag') or temp_link.__contains__('business.instagram')
                    or temp_link.__contains__('m.facebook') or temp_link.__contains__(
                        '?locale') or temp_link.__contains__('/search')):
                return True
            else:
                return False

        changed = False
        new_list = [link for link in company['Links'] if not rem_link(link)]
        if len(new_list) != len(company['Links']):
            company['Links'] = new_list
            changed = True

        for media_link in company['Links']:
            if media_link is None:
                print(company['id'])
            if media_link.__contains__('.instagram.com'):
                no_ig_link = False
            if media_link.__contains__('.facebook.com'):
                no_fb_link = False

        try:
            if no_fb_link:
                fb_link = get_facebook_link(company['Name'])
                if fb_link is not None:
                    fb_link = fb_link.replace("m.facebook", "www.facebook")

                    indx = fb_link.find('?locale')
                    if indx != -1:
                        fb_link = fb_link[:indx]

                    company['Links'].append(fb_link)
        except:
            print("couldn't get facebook link")

        try:
            if no_ig_link:
                ig_link = get_instagram_link(company['Name'])
                if ig_link is not None:
                    company['Links'].append(ig_link)
        except:
            print("couldn't get instagram link")

        if no_ig_link or no_fb_link or changed:
            supabase.table('Companies').update({'Links': company['Links']}).eq('id', company['id']).execute()
            print(f"added links for company {company['Name']}: {company['Links']}")
        else:
            print("already has both links")

        if changed:
            print(f"{company['Name']} had an error in it's links list")

        companies_done += 1
        if companies_done % 10 == 0:
            print((companies_done / total_companies) * 100)


def get_facebook_link(name):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_query = name + " Facebook"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        attrib = link.get_attribute('href')
        if (attrib is not None and attrib.__contains__('.facebook.com') and not attrib.__contains__(
                '/photo') and not attrib.__contains__('/post') and not attrib.__contains__('/video') and
                not attrib.__contains__('/hashtag') and not attrib.__contains__('/search')):
            return attrib


def get_instagram_link(name):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_query = name + " Instagram"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        attrib = link.get_attribute('href')
        if (attrib is not None and attrib.__contains__('.instagram.com') and not attrib.__contains__(
                '/p/') and not attrib.__contains__('/explore/') and not attrib.__contains__('business.instagram')):
            return attrib


main_func()
