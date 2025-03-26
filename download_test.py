import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    # Указываем папку для загрузок
    download_path = os.path.abspath("downloads")
    os.makedirs(download_path, exist_ok=True)

    # Настройки Chrome для скачивания файлов без запроса
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_download_plugin(driver):
    # 1. Открываем сайт СБИС
    driver.get("https://sbis.ru/")

    # 2. Переходим в "Скачать локальные версии"
    driver.find_element(By.LINK_TEXT, "Скачать локальные версии").click()

    # 3. Кликаем по кнопке скачивания плагина для Windows
    plugin = driver.find_element(By.XPATH, "//a[contains(@href, 'sbisplugin') and contains(text(), 'Windows')]")
    download_url = plugin.get_attribute("href")
    file_name = os.path.basename(download_url)

    # 4. Скачиваем плагин
    driver.get(download_url)
    file_path = os.path.join("downloads", file_name)

    # 5. Проверяем, что файл скачался
    assert os.path.exists(file_path), "Файл не скачался"

    # 6. Проверяем размер файла
    actual_size = os.path.getsize(file_path) / (1024 * 1024)  # Размер в МБ
    expected_size = 3.64  # Размер с сайта
    assert abs(actual_size - expected_size) < 0.1, "Размер файла не совпадает"
