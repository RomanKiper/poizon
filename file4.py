import os.path
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# Function to write links to a file
def write_links_to_file(links):
    with open('links.txt', 'a') as file:
        for link in links:
            file.write(link + '\n')

# Check if the file exists and load existing links
existing_links = set()
if os.path.exists('links.txt'):
    with open('links.txt', 'r') as file:
        existing_links = set(file.read().splitlines())

# Iterate over all available pages
for page in range(1, 21):  # Adjusted the range to iterate over all 20 pages
    driver.get(f'https://www.poizon.com/category/sneakers-500000091?page={page}')
    time.sleep(5)
    second_step = driver.find_elements(By.XPATH, "//div[@class='PoizonImage_imageWrap__RZTiw']")
    second_step[6].click()
    second_step[7].click()
    time.sleep(5)
    html = driver.find_elements(By.CLASS_NAME, 'GoodsItem_goodsItem__pfNZb')

    # Iterate through the elements on the page
    for element in html:
        href = element.get_attribute('href')
        if "adidas" in href:
            print(href, type(href))
            # Check if the link is already in the existing links
            if href not in existing_links:
                # If not, add it to the existing links and write to the file
                existing_links.add(href)
                write_links_to_file([href])
                print(f"New link added: {href}")

# Close the browser
driver.quit()