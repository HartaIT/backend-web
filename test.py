import time

from selenium.webdriver import Keys
from Utils import webdriver_setup
from selenium.webdriver.common.by import By
import os

from dotenv import load_dotenv

load_dotenv()

from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# driver = webdriver_setup.get_driver(True, True, False)
#
# driver.get("https://www.linkedin.com/login")
# driver.add_cookie({
#     "name": "li_at",
#     "value": "AQEDAUZ0w2ED5qfsAAABimXlnHgAAAGKifIgeFYAJ9lRm6sJMk_STxwM6QkIIHDhLEiM_7VRriZmNuP9Ts7Ti5bc13DpyDyb0YVBLUZrD0E-ilr8D2qFt7CG8xk5v1BebubrFSRtpQS0ggPTOED2p42t"
# })
# time.sleep(50)

# post = supabase.table('Posts').select('*').eq('id', 72).execute().data[0]
# supabase.table('Posts').update(
#         {'City': list(set(post['City'])),
#          'Keywords': list(set(post['Keywords']))}
#     ).eq('id', post['id']).execute()

driver = webdriver_setup.get_driver(False, False, False)
driver.get("https://www.google.com")
buttons = driver.find_elements(By.TAG_NAME, "button")[3].click()

search_box = driver.find_element(By.NAME, "q")

search_query = "NetRom Software" + " Facebook Romania"
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    attrib = link.get_attribute('href')
    if attrib is not None and attrib.__contains__('facebook'):
        print(link.get_attribute('href'))
        break

time.sleep(120)
