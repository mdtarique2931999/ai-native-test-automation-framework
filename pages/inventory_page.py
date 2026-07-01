from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")

    def wait_for_products(self):
        return self.wait_for_all(self.INVENTORY_ITEMS)

    def get_product_names(self):
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def get_product_prices(self):
        return [el.text for el in self.driver.find_elements(*self.ITEM_PRICES)]

    def sort_by(self, option_text):
        dropdown = self.wait_for(self.SORT_DROPDOWN)
        Select(dropdown).select_by_visible_text(option_text)

    def set_viewport(self, width, height):
        self.driver.set_window_size(width, height)

    def get_visible_item_count(self):
        return len(self.driver.find_elements(*self.INVENTORY_ITEMS))

    def is_menu_visible(self):
        return self.driver.find_element(*self.MENU_BUTTON).is_displayed()
