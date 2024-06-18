test_case_id,username,password,expected_result
TC_Login_01,Admin,admin123,Success
TC_Login_02,Admin,invalid_password,Invalid credentials
TC_PIM_01,Admin,admin123,Add Employee Success
TC_PIM_02,Admin,admin123,Edit Employee Success
TC_PIM_03,Admin,admin123,Delete Employee Success

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

from selenium.webdriver.common.by import By
from pages.base_page.py import BasePage

class LoginPage(BasePage):
    username_input = (By.ID, "txtUsername")
    password_input = (By.ID, "txtPassword")
    login_button = (By.ID, "btnLogin")
    error_message = (By.ID, "spanMessage")

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text

from selenium.webdriver.common.by import By
from pages.base_page.py import BasePage

class PIMPage(BasePage):
    pim_module = (By.ID, "menu_pim_viewPimModule")
    add_employee_button = (By.ID, "btnAdd")
    first_name_input = (By.ID, "firstName")
    last_name_input = (By.ID, "lastName")
    save_button = (By.ID, "btnSave")
    success_message = (By.CSS_SELECTOR, ".message.success")

    def navigate_to_pim(self):
        self.driver.find_element(*self.pim_module).click()

    def add_employee(self, first_name, last_name):
        self.driver.find_element(*self.add_employee_button).click()
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.save_button).click()

    def get_success_message(self):
        return self.driver.find_element(*self.success_message).text

import csv

def read_test_data(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

import pytest
from pages.login_page import LoginPage
from utils.data_reader import read_test_data

test_data = read_test_data("data/test_data.csv")

@pytest.mark.parametrize("data", test_data)
def test_login(browser, data):
    login_page = LoginPage(browser)
    if "Login" in data["test_case_id"]:
        login_page.login(data["username"], data["password"])
        if data["expected_result"] == "Success":
            assert browser.current_url == "expected_homepage_url"  # Replace with actual URL after successful login
        else:
            assert login_page.get_error_message() == data["expected_result"]

import pytest
from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.data_reader import read_test_data

test_data = read_test_data("data/test_data.csv")

@pytest.mark.parametrize("data", test_data)
def test_pim(browser, data):
    login_page = LoginPage(browser)
    pim_page = PIMPage(browser)

    if "PIM" in data["test_case_id"]:
        login_page.login(data["username"], data["password"])
        pim_page.navigate_to_pim()

        if data["test_case_id"] == "TC_PIM_01":
            pim_page.add_employee("John", "Doe")
            assert pim_page.get_success_message() == "Add Employee Success"
        elif data["test_case_id"] == "TC_PIM_02":
            # Implement Edit Employee details and validation
            pass
        elif data["test_case_id"] == "TC_PIM_03":
            # Implement Delete Employee details and validation
            pass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))


from selenium.webdriver.common.by import By
from pages.base_page.py import BasePage

class PIMPage(BasePage):
    pim_module = (By.ID, "menu_pim_viewPimModule")
    add_employee_button = (By.ID, "btnAdd")
    first_name_input = (By.ID, "firstName")
    last_name_input = (By.ID, "lastName")
    save_button = (By.ID, "btnSave")
    success_message = (By.CSS_SELECTOR, ".message.success")

    def navigate_to_pim(self):
        self.driver.find_element(*self.pim_module).click()

    def add_employee(self, first_name, last_name):
        self.driver.find_element(*self.add_employee_button).click()
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.save_button).click()

    def get_success_message(self):
        return self.driver.find_element(*self.success_message).text
