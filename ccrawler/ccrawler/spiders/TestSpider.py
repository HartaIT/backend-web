from __future__ import absolute_import

import scrapy, json
import requests
from scrapy import FormRequest
from w3lib.html import replace_escape_chars
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from ..items import CompanyItem
from bs4 import BeautifulSoup
from scrapy.selector import Selector



class TestSpider(scrapy.Spider):
    name = "TestSpider"

    start_urls = ['https://api.ipify.org']


    def parse(self, response):
        self.driver_opened = True
        driver = webdriver.Chrome()
        driver.implicitly_wait(4)

        response = response.replace(body=self.driver.page_source)

        yield {"test": response.text}