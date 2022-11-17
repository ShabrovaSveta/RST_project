import myutils
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

URL_REGISTRATION = ''
URL_AUTH = 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&auth_type'

FIRST_NAME = 'Светлана'
LAST_NAME = 'Шаброва'

PASSWORD = '8@H46pcRbcyWaxJ'
EMAIL = 'svetatest@gmail.com'
PHONE = '+7 922 522-83-33'

# Неправильные данные для негативного теста.
WRONG_EMAIL = 'svetatesttest@gmail.com'
WRONG_PASSWORD = '8qwertY57'
SHORT_PASSWORD = '8@H46p'
LONG_PASSWORD = '8@H46pcRbcyWaxJ8@H46pcRbcyWaxJ'
SMALL_LETTERS_PASSWORD = '8dghkcsdjk'
CYRILLIC_PASSWORD = '8привет!'
LATIN_FIRST_NAME = 'Svetlana'
LATIN_LAST_NAME = 'Shabrova'
EMPTY_PHONE = ''
EMPTY_PASSWORD = ''
EMPTY_EMAIL = ''


WRONG_LOGIN_PASS_MESSAGE = 'Неверный логин или пароль'
SHORT_PASSWORD_MESSAGE = 'Длина пароля должна быть не менее 8 символов'
LONG_PASSWORD_MESSAGE = 'Длина пароля должна быть не более 20 символов'
SMALL_LETTERS_PASSWORD_MESSAGE = 'Пароль должен содержать хотя бы одну заглавную букву'
CYRILLIC_PASSWORD_MESSAGE = 'Пароль должен содержать только латинские буквы'
LATIN_FIRST_LAST_NAME_MESSAGE = 'Необходимо заполнить поле кириллицей. От 2 до 30 символов'
ENTER_NUMBER_PHONE_MESSAGE = 'Введите номер телефона'
ENTER_EMAIL = 'Введите адрес, указанный при регистрации'
ENTER_PASSWORD = 'Введите пароль, указанный при регистрации'

# Регистрация пользователя с корректными данными.
def test_001_correct_registration(driver):
    # Переходим на страницу регистрации
    url = 'https://b2c.passport.rt.ru/'
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'kc-register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'firstName'))).send_keys(FIRST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'lastName'))).send_keys(LAST_NAME)
    # ВНИМАНИЕ! На форме регистрации есть ещё выпадающий список "Регион",
    # но у него не нашла ни ID, ни NAME, ни уникальный класс. Возможно что-то не понимаю, возможно баг.
    # Но при регистрации это поле корректно сохраняется в учётке.
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'address'))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password'))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password-confirm'))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'register'))).click()

    # Ввод шестизначного кода подтверждения. Он уходит на email
    # Ищем первое из шести полей ввод, его ID = "rt-code-0". Следующее "rt-code-1", "rt-code-2" и т.п.
    CONFIRM_CODE = '123456'  # Делаем вид будто у нас есть этот код, это строка из 6 символов.
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'rt-code-0'))).send_keys(CONFIRM_CODE[0])
    driver.find_element(By.ID, 'rt-code-1').send_keys(CONFIRM_CODE[1])
    driver.find_element(By.ID, 'rt-code-2').send_keys(CONFIRM_CODE[2])
    driver.find_element(By.ID, 'rt-code-3').send_keys(CONFIRM_CODE[3])
    driver.find_element(By.ID, 'rt-code-4').send_keys(CONFIRM_CODE[4])
    driver.find_element(By.ID, 'rt-code-5').send_keys(CONFIRM_CODE[5])
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    time.delay(5)
    assert myutils.get_relative_link(driver) == '/account_b2c/page'


# Регистрация пользователя с паролем менее 8 символов
def test_002_short_password(driver):
    url = 'https://b2c.passport.rt.ru/'
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'kc-register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'firstName'))).send_keys(FIRST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'lastName'))).send_keys(LAST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'address'))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password'))).send_keys(SHORT_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password-confirm'))).send_keys(SHORT_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == SHORT_PASSWORD_MESSAGE


# Регистрация пользователя с паролем более 20 символов
def test_003_long_password(driver):
    url = 'https://b2c.passport.rt.ru/'
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'kc-register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'firstName'))).send_keys(FIRST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'lastName'))).send_keys(LAST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'address'))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password'))).send_keys(LONG_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password-confirm'))).send_keys(LONG_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == LONG_PASSWORD_MESSAGE


# Регистрация пользователя с паролем с использованием маленьких букв
def test_004_small_letters_password(driver):
    url = 'https://b2c.passport.rt.ru/'
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'kc-register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'firstName'))).send_keys(FIRST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'lastName'))).send_keys(LAST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'address'))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password'))).send_keys(SMALL_LETTERS_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password-confirm'))).send_keys(SMALL_LETTERS_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == SMALL_LETTERS_PASSWORD_MESSAGE


# Регистрация пользователя с паролем с использованием кириллицы
def test_005_cyrillic_password(driver):
    url = 'https://b2c.passport.rt.ru/'
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'kc-register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'firstName'))).send_keys(FIRST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'lastName'))).send_keys(LAST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'address'))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password'))).send_keys(CYRILLIC_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password-confirm'))).send_keys(CYRILLIC_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == CYRILLIC_PASSWORD_MESSAGE


# Регистрация пользователя с латинским именем/фамилией
def test_006_latin_first_last_name(driver):
    url = 'https://b2c.passport.rt.ru/'
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'kc-register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'firstName'))).send_keys(LATIN_FIRST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'lastName'))).send_keys(LATIN_LAST_NAME)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'address'))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password'))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'password-confirm'))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, 'register'))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == LATIN_FIRST_LAST_NAME_MESSAGE


# Авторизация пользователя с корректными данными
def test_007_login_by_phone(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "username"))).send_keys(PHONE)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "kc-login"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    assert myutils.get_relative_link(driver) == '/account_b2c/page'

# Авторизация пользователя с корректными данными
def test_008_login_by_email(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "username"))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "kc-login"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    assert myutils.get_relative_link(driver) == '/account_b2c/page'


# Авторизация пользователя с некорректными данными
def test_009_login_by_wrong_email(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "username"))).send_keys(WRONG_EMAIL)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "password"))).send_keys(WRONG_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "kc-login"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "card-container__error")))
    system_message = driver.find_elements(By.CLASS_NAME, 'card-container__error')
    system_message = system_message[0].text
    assert system_message == WRONG_LOGIN_PASS_MESSAGE


# Авторизация пользователя с пустым полем "Мобильный телефон"
def test_010_login_without_phone(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "username"))).send_keys(EMPTY_PHONE)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "kc-login"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == ENTER_NUMBER_PHONE_MESSAGE

#Авторизация пользователя с пустым полем "Пароль"
def test_011_login_without_password(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "username"))).send_keys(PHONE)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "password"))).send_keys(EMPTY_PASSWORD)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "kc-login"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == ENTER_PASSWORD


#Авторизация пользователя с пустым полем "Электронная почта"
def test_012_login_without_email(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "oidc_oke"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "//*[@id="widget-el"]/div[2]/div[1]/div[1]"))).clicl()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "kc-login"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta")))
    system_message = driver.find_elements(By.CLASS_NAME, 'rt-input-container__meta')
    system_message = system_message[0].text
    assert system_message == ENTER_EMAIL


# Авторизация пользователя с помощью соцсетей ВК
def test_013_authorization_cosial_networks_VK(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "oidc_vk"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "oauth_wrap_content"))).click()
    DriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    assert myutils.get_relative_link(driver) == '/account_b2c/page'


# Авторизация пользователя с помощью соцсетей OK
def test_014_authorization_cosial_networks_OK(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "oidc_ok"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "widget-oauth"))).click()
    DriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    assert myutils.get_relative_link(driver) == '/account_b2c/page'


# Авторизация пользователя с помощью соцсетей Мой Мир
def test_014_authorization_cosial_networks_mail(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "oidc_mail"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "wrp"))).click()
    DriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    assert myutils.get_relative_link(driver) == '/account_b2c/page'

# Авторизация пользователя с помощью соцсетей Google
def test_015_authorization_cosial_networks_google(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "oidc_google"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "_gd"))).click()
    DriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    assert myutils.get_relative_link(driver) == '/account_b2c/page'

# Авторизация пользователя с помощью соцсетей Яндекс
def test_015_authorization_cosial_networks_yandex(driver):
    driver.get(URL_AUTH)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "oidc_google"))).click()
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "passp-page"))).click()
    DriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "user-contacts-item__value")))
    assert myutils.get_relative_link(driver) == '/account_b2c/page'
