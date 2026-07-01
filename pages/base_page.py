import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self, path=""):
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.driver.get(url)

    def wait_for(self, locator, timeout=None):
        timeout = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_all(self, locator, timeout=None):
        timeout = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def save_screenshot(self, name):
        reports_dir = os.path.join(os.getcwd(), "reports", "screenshots")
        os.makedirs(reports_dir, exist_ok=True)
        path = os.path.join(reports_dir, f"{name}.png")
        self.driver.save_screenshot(path)
        return path
