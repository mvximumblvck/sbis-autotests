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

def test_tensor_page(driver):
    # 1. Открываем СБИС и переходим в "Контакты"
    driver.get("https://sbis.ru/")
    driver.find_element(By.LINK_TEXT, "Контакты").click()

    # 2. Находим баннер "Тензор" и кликаем по нему
    tensor_banner = driver.find_element(By.CSS_SELECTOR, "a[href='https://tensor.ru/']")
    tensor_banner.click()

    # 3. Проверяем, что на Tensor есть блок "Сила в людях"
    driver.get("https://tensor.ru/")
    assert driver.find_element(By.XPATH, "//h2[contains(text(), 'Сила в людях')]"), "Блок 'Сила в людях' не найден"

    # 4. Переходим в "Подробнее"
    driver.find_element(By.LINK_TEXT, "Подробнее").click()

    # 5. Проверяем, что открылась страница "О компании"
    assert "about" in driver.current_url, "Страница 'О компании' не открылась"
