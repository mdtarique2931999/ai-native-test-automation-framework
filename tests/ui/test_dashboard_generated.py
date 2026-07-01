import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def _login_as(driver, base_url, username):
    login_page = LoginPage(driver, base_url)
    login_page.login(username, "secret_sauce")
    return InventoryPage(driver, base_url)


@pytest.mark.ui
def test_widget_loading(driver, base_url):
    inventory = _login_as(driver, base_url, "standard_user")
    products = inventory.wait_for_products()
    assert len(products) >= 6


@pytest.mark.ui
def test_data_accuracy(driver, base_url):
    inventory = _login_as(driver, base_url, "standard_user")
    inventory.wait_for_products()
    names = inventory.get_product_names()
    prices = inventory.get_product_prices()
    assert names[0] == "Sauce Labs Backpack"
    assert prices[0] == "$29.99"


@pytest.mark.ui
def test_sort_by_price_high_to_low(driver, base_url):
    inventory = _login_as(driver, base_url, "standard_user")
    inventory.wait_for_products()
    inventory.sort_by("Price (high to low)")
    prices = inventory.get_product_prices()
    numeric_prices = [float(price.replace("$", "")) for price in prices]
    assert numeric_prices[0] == max(numeric_prices)


@pytest.mark.ui
def test_responsive_layout(driver, base_url):
    inventory = _login_as(driver, base_url, "standard_user")
    inventory.wait_for_products()
    inventory.set_viewport(375, 667)
    assert inventory.get_visible_item_count() >= 1
    assert inventory.is_menu_visible()


@pytest.mark.ui
def test_permission_based_visibility(driver, base_url):
    standard_inventory = _login_as(driver, base_url, "standard_user")
    standard_inventory.wait_for_products()
    standard_count = standard_inventory.get_visible_item_count()

    driver.delete_all_cookies()
    driver.get(base_url)

    problem_inventory = _login_as(driver, base_url, "problem_user")
    problem_inventory.wait_for_products()
    problem_count = problem_inventory.get_visible_item_count()

    assert standard_count == problem_count
