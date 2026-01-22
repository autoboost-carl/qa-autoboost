import pytest
from playwright.sync_api import Page

from pages.HomePage import HomePage
from pages.LoginPage import LoginPage

URL = "https://www.automationteststore.com"


@pytest.mark.smoke
def test_login(page: Page, credentials: dict):
    """Smoke test: login flow using POMs.

    Steps:
    1) navega a la URL
    2) haz click en el boton de login
    3) llena "Login Name"
    4) llena "Password"
    5) haz click en login

    Resultado esperado: estar en "My Account"
    """
    login_name = credentials.get("LOGIN_NAME")
    password = credentials.get("LOGIN_PASSWORD")

    if not login_name or not password:
        pytest.skip("Set LOGIN_NAME and LOGIN_PASSWORD environment variables or fill data/credentials.env to run this test")

    home = HomePage(page, base_url=URL)
    home.goto()
    home.open_login()

    login = LoginPage(page)
    login.login(login_name, password)

    assert login.is_my_account_visible()
