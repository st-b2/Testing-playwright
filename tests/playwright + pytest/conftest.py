import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getini("base_url")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pl:
        browser = pl.chromium.launch(
            headless=False,
            slow_mo=500
        )
        yield browser
        browser.close()

@pytest.fixture
def page(browser, base_url):
    page = browser.new_page()
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    yield page
    page.close()