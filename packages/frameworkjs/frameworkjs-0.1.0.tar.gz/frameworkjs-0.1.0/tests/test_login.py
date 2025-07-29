# tests/test_login.py

import pytest
from selenium import webdriver
from yourpackage.base_page import BasePage
from selenium.webdriver.common.by import By

def test_login():
    driver = webdriver.Chrome()
    page = BasePage(driver)
    page.open_url("https://example.com/login")
    page.send_text(By.ID, "username", "admin")
    page.send_text(By.ID, "password", "secret")
    page.click_element(By.ID, "submit")
    driver.quit()
