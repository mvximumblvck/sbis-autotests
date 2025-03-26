import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

def test_change_region(driver):
    # 1. Открываем СБИС и переходим в "Контакты"
    driver.get("https://sbis.ru/")
    driver.find_element(By.LINK_TEXT, "Контакты").click()

    # 2. Проверяем текущий регион
    current_region = driver.find_element(By.CLASS_NAME, "sbis_ru-Region-Chooser__text").text
    assert current_region, "Регион не определился"

    # 3. Меняем регион на Камчатский край
    driver.find_element(By.CLASS_NAME, "sbis_ru-Region-Chooser__text").click()
    driver.find_element(By.LINK_TEXT, "Камчатский край").click()

    # 4. Проверяем, что регион изменился
    new_region = driver.find_element(By.CLASS_NAME, "sbis_ru-Region-Chooser__text").text
    assert new_region == "Камчатский край", "Регион не изменился"

    # 5. Проверяем, что изменился список партнеров
    partners_list = driver.find_elements(By.CLASS_NAME, "sbis_ru-Contacts-Promo__list")
    assert len(partners_list) > 0, "Список партнеров не изменился"

    # 6. Проверяем URL и заголовок
    assert "kamchatskij-kraj" in driver.current_url, "URL не изменился"
    assert "Камчатский край" in driver.title, "Title не изменился"
