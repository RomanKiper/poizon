import os.path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Инициализация веб-драйвера
driver = webdriver.Chrome()


# Функция для записи ссылок в файл
def write_links_to_file(links):
    with open('links2.txt', 'a') as file:
        for link in links:
            file.write(link + '\n')


# Проверка наличия файла и загрузка существующих ссылок
existing_links = set()
if os.path.exists('links2.txt'):
    with open('links2.txt', 'r') as file:
        existing_links = set(file.read().splitlines())

# Итерация по всем доступным страницам
for page in range(1, 21):  # Изменили диапазон, чтобы пройти по всем 20 страницам
    # Получаем содержимое страницы
    driver.get(f'https://www.poizon.com/category/sneakers-500000091?page={page}')

    try:
        # Ожидание появления элементов для клика
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='PoizonImage_imageWrap__RZTiw']"))
        )

        # Находим нужные элементы на странице
        second_step = driver.find_elements(By.XPATH, "//div[@class='PoizonImage_imageWrap__RZTiw']")
        # Выполняем клики, чтобы загрузить полное содержимое страницы
        second_step[6].click()
        second_step[7].click()

        # Ожидание загрузки контента
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'GoodsItem_goodsItem__pfNZb'))
        )

        # Дополнительное ожидание после кликов
        time.sleep(2)

        # Находим все элементы с ссылками на товары
        html = driver.find_elements(By.CLASS_NAME, 'GoodsItem_goodsItem__pfNZb')

        # Итерируемся по элементам на странице
        for element in html:
            href = element.get_attribute('href')
            # Проверяем, содержит ли ссылка "adidas" и не была ли она уже записана
            if "adidas" in href and href not in existing_links:
                existing_links.add(href)
                write_links_to_file([href])
                print(f"Новая ссылка добавлена: {href}")
    except TimeoutException as e:
        print(f"TimeoutException: {e}")
        print(f"Current page URL: {driver.current_url}")

# Закрываем браузер
driver.quit()