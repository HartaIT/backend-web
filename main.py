from dotenv import load_dotenv
from fastapi import FastAPI
from selenium import webdriver

load_dotenv()

app = FastAPI()

driver = webdriver.Chrome()


@app.get("/get/{url}")
async def get_url(url: str):
    url = 'https://' + url
    driver.get(url)
