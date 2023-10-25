from __future__ import absolute_import
from pathlib import Path
import scrapy, json
from unidecode import unidecode
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json



load_dotenv()

from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

path = Path(__file__).parents[2] / "files\\Cities.json"

file = open(path)
cities_array = json.load(file)


class LICompanyScraper(scrapy.Spider):
    name = "LICompanyScraper"
    start_urls = ['https://www.linkedin.com/company/microsoft']

    def parse(self, response):
        pass
