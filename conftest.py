import os

import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.failure_explainer import build_and_explain

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com")


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL", "https://reqres.in/api")


@pytest.fixture
def driver(base_url):
    options = Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(3)
    browser.get(base_url)
    yield browser
    browser.quit()


@pytest.fixture
def api_client(api_base_url):
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = api_base_url
    return session


def _api_url(api_client, path):
    return f"{api_client.base_url}/{path.lstrip('/')}"


@pytest.fixture
def api_get(api_client):
    def _get(path, **kwargs):
        response = api_client.get(_api_url(api_client, path), **kwargs)
        api_client.last_response = response
        return response

    return _get


@pytest.fixture
def api_post(api_client):
    def _post(path, json=None, **kwargs):
        response = api_client.post(_api_url(api_client, path), json=json, **kwargs)
        api_client.last_response = response
        return response

    return _post


@pytest.fixture
def api_put(api_client):
    def _put(path, json=None, **kwargs):
        response = api_client.put(_api_url(api_client, path), json=json, **kwargs)
        api_client.last_response = response
        return response

    return _put


@pytest.fixture
def api_delete(api_client):
    def _delete(path, **kwargs):
        response = api_client.delete(_api_url(api_client, path), **kwargs)
        api_client.last_response = response
        return response

    return _delete


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver")
    api_client = item.funcargs.get("api_client")
    api_response = getattr(api_client, "last_response", None) if api_client else None

    explanation, output_path = build_and_explain(
        item, report, driver=driver, api_response=api_response
    )
    report.llm_explanation = explanation
    report.llm_output_path = output_path

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is not None:
        extras = getattr(report, "extra", [])
        extras.append(pytest_html.extras.text(explanation, name="LLM Failure Explanation"))
        report.extra = extras
