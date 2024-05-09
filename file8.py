import os
import time
import requests
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Определяем относительные пути для временной папки и папки с изображениями
temp_dir = os.path.join('temp_images', '')
image_dir = 'images'

# Проверяем наличие папки для сохранения изображений, и создаем ее при необходимости
if not os.path.exists(image_dir):
    os.makedirs(image_dir)



# Инициализация веб-драйвера
driver = webdriver.Chrome()

# Функция для загрузки изображения
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

# Проверка наличия файла и загрузка существующих ссылок
existing_links = set()
if os.path.exists('links2.txt'):
    with open('links2.txt', 'r') as file:
        existing_links = set(file.read().splitlines())

links_to_process = list(existing_links)[:5]

# Создаем новую книгу Excel и активный лист
wb = Workbook()
ws = wb.active

# Заголовки столбцов
ws.append(["Ссылка на товар", "Наименование", "Цена в usd", "Brand", "Style", "Release Date", "Sole Material", "Upper Material", "Изображения"])

# Итерация по каждой ссылке
for link in links_to_process:
    driver.get(link)

    try:
        # Ожидание загрузки данных о товаре
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'GoodsDetail_wrapper__tZh3Z'))
        )
        time.sleep(5)

        # Получаем данные о товаре
        product_details = {}

        # Наименование товара
        product_name = driver.find_element(By.CLASS_NAME, 'MainInfo_title__YSsXk').text

        # Стоимость товара
        price_bar = driver.find_element(By.CLASS_NAME, 'MainInfo_priceBar__tcUgc')
        price_div = price_bar.find_element(By.TAG_NAME, 'div')
        product_price = price_div.text.replace('$', '')

        # Находим все элементы с классом 'ProductDetails_propertyItem__mGdzY'
        product_items = driver.find_elements(By.CLASS_NAME, 'ProductDetails_propertyItem__mGdzY')

        # Переменные для хранения значений
        product_brand = ""
        product_style = ""
        product_release_date = ""
        product_sole_material = ""
        product_upper_material = ""

        # Проходим по найденным элементам
        for item in product_items:
            # Находим элементы с классом 'ProductDetails_propertyLabel__ZlSsu'
            label = item.find_element(By.CLASS_NAME, 'ProductDetails_propertyLabel__ZlSsu').text
            # Находим элементы с классом 'ProductDetails_propertyValue__Aj_Cz'
            value = item.find_element(By.CLASS_NAME, 'ProductDetails_propertyValue__Aj_Cz').text
            # Проверяем, что текст элемента соответствует "Brand"
            if label == "Brand":
                product_brand = value
            # Проверяем, что текст элемента соответствует "Style"
            elif label == "Style":
                product_style = value
            elif label == "Release Date":
                product_release_date = str(value)
            elif label == "Sole Material":
                product_sole_material = str(value)
            elif label == "Upper Material":
                product_upper_material = str(value)

        # Получаем ссылки на изображения
        image_elements = driver.find_elements(By.XPATH, '//img[@class="PoizonImage_img__BNSaU ProductSkuImgs_img__gYd8t"]')  # Пример XPath

        # Список для хранения ссылок на изображения
        image_urls = []

        # Сохраняем изображения
        for index, image_element in enumerate(image_elements, start=1):
            image_url = image_element.get_attribute('src')
            image_url = image_url.replace("w_160", "w_800")
            print(image_url)

            image_filename = f"{product_name.replace(' ', '_')}_{index}.png"
            image_path = os.path.join(image_dir, image_filename)
            download_image(image_url, image_path)
            print(f"Сохранено изображение: {image_filename}")  # Отладочный вывод
            image_urls.append(image_path)

        # Запись данных о товаре в Excel
        ws.append([link, product_name, product_price, product_brand, product_style, product_release_date, product_sole_material,
                   product_upper_material, '\n'.join(image_urls)])

    except TimeoutException as e:
        print(f"TimeoutException: {e}")
        print(f"Current page URL: {driver.current_url}")

# Создаем папку "output" для сохранения файла Excel, если она еще не существует
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Сохраняем книгу Excel
wb.save(os.path.join(output_dir, 'product_details.xlsx'))

# Закрываем браузер
driver.quit()
