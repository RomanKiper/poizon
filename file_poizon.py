import os.path

from selenium import webdriver
import time
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

for page in range(1, 20):
    first_step = driver.get(f'https://www.poizon.com/category/sneakers-500000091?page={page}')
    time.sleep(2)
    second_step = driver.find_elements(By.XPATH, "//div[@class='PoizonImage_imageWrap__RZTiw']")
    second_step[6].click()
    second_step[7].click()
    time.sleep(2)
    html = driver.find_elements(By.CLASS_NAME, 'GoodsItem_goodsItem__pfNZb')
    # print(len(html))

    for element in html:
        html_code = element.get_attribute('outerHTML')
        print(html_code)

