import pytest

from pages.login_page import LoginPage


@pytest.mark.ui
def test_valid_login(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in()


@pytest.mark.ui
def test_invalid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.login("standard_user", "wrong_password")
    error = login_page.get_error_message()
    assert "Epic sadface" in error
    assert "do not match" in error


@pytest.mark.ui
def test_forgot_password_not_available(driver, base_url):
    login_page = LoginPage(driver, base_url)
    assert login_page.has_forgot_password_link() is False


@pytest.mark.ui
def test_session_expiry_redirects_to_login(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in()

    driver.delete_all_cookies()
    driver.get(f"{base_url}/inventory.html")

    assert "inventory.html" not in driver.current_url
    assert driver.find_elements(*LoginPage.USERNAME)


@pytest.mark.ui
def test_locked_out_user(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.login("locked_out_user", "secret_sauce")
    error = login_page.get_error_message()
    assert "locked out" in error.lower()
