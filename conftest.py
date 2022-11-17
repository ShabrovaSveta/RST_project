import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options


@pytest.fixture
def get_chrome_options():
    # Настройки драйвера
    options = chrome_options()
    options.add_argument('chrome')
    options.add_argument('--start-maximized')  # Окно браузера будет развёрнуто на весь экран.
    return options


@pytest.fixture(scope='function', autouse=True)
def driver(get_chrome_options):
    # Получение экземпляра вебдрайвера с учётом настроек.
    options = get_chrome_options
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
