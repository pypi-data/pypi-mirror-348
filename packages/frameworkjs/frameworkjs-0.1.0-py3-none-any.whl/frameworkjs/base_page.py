# your_package/base_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import string

from .logger import BaseLogging  # logger class

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = BaseLogging()

    def send_text(self, by, value, text):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"✅ Sent text '{text}' to element {value}")

    # Include all your other methods here...
