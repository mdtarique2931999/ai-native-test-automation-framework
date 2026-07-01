from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")

    def login(self, username, password):
        self.wait_for(self.USERNAME).clear()
        self.wait_for(self.USERNAME).send_keys(username)
        self.wait_for(self.PASSWORD).clear()
        self.wait_for(self.PASSWORD).send_keys(password)
        self.wait_for(self.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.wait_for(self.ERROR_MESSAGE).text

    def is_logged_in(self):
        return len(self.driver.find_elements(*self.INVENTORY_CONTAINER)) > 0

    def has_forgot_password_link(self):
        links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "password")
        return any("forgot" in link.text.lower() for link in links)
