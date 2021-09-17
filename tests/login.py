from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from os import environ

WHITE_COLOR = "\033[0m"
RED_COLOR = "\033[31m"
GREEN_COLOR = "\033[32m"

CHROMEDRIVER_EXECUTABLE_PATH = environ.get("CHROMEDRIVER_EXECUTABLE_PATH")
BX_LOGIN_URL = environ.get("BX_LOGIN_URL")
BX_LOGIN_TEST_EMAIL = environ.get("BX_LOGIN_TEST_EMAIL")
BX_LOGIN_TEST_PASSWORD = environ.get("BX_LOGIN_TEST_PASSWORD")

options = webdriver.ChromeOptions()

# No GUI
options.add_argument("headless")

# Able to run as root user
options.add_argument("no-sandbox")

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_EXECUTABLE_PATH, options=options)
driver.implicitly_wait(5)

try:
    driver.get(BX_LOGIN_URL)

    username = driver.find_element(By.ID, "id_username")
    username.send_keys(BX_LOGIN_TEST_EMAIL)

    password = driver.find_element(By.ID, "id_password")
    password.send_keys(BX_LOGIN_TEST_PASSWORD, Keys.ENTER)

    driver.implicitly_wait(5)
    logged_email = driver.find_element(By.XPATH, "//a[@class='dropdown-button btn-flat blue-text']").text
    sleep(5)

    assert logged_email == BX_LOGIN_TEST_EMAIL.upper(), f"{BX_LOGIN_TEST_EMAIL.upper()} was expected as logged user"
    print(f"{GREEN_COLOR}[SUCCESS] Login test case passed{WHITE_COLOR}")
except Exception as e:
    print(f"{RED_COLOR}[ERROR] {str(e)}{WHITE_COLOR}")
    raise e

driver.quit()