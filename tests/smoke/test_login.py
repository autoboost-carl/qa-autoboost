import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@pytest.mark.smoke
@pytest.mark.p0
def test_login_page_elements_visible(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    
    assert login_page.login_name_input.is_visible(), "Login name input is not visible"
    assert login_page.password_input.is_visible(), "Password input is not visible"
    assert login_page.login_button.is_visible(), "Login button is not visible"
    assert login_page.forgot_password_link.is_visible(), "Forgot password link is not visible"

    print("All login page elements are visible.")

@pytest.mark.smoke
@pytest.mark.p0
def test_login_with_valid_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    
    valid_login_name = os.getenv("VALID_LOGIN_NAME")
    valid_password = os.getenv("VALID_PASSWORD")
    
    login_page.enter_login_name(valid_login_name)
    login_page.enter_password(valid_password)
    login_page.click_login_button()
    
    login_page.assert_login_successful()

    print("Login with valid credentials successful.")

@pytest.mark.smoke
@pytest.mark.p0
def test_login_with_invalid_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    
    invalid_login_name = os.getenv("INVALID_LOGIN_NAME")
    invalid_password = os.getenv("INVALID_PASSWORD")
    
    login_page.enter_login_name(invalid_login_name)
    login_page.enter_password(invalid_password)
    login_page.click_login_button()
    
    login_page.assert_error_displayed()

    print("Login with invalid credentials displayed error as expected.")

@pytest.mark.smoke
@pytest.mark.p0
def test_login_with_empty_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    
    empty_login_name = os.getenv("EMPTY_LOGIN_NAME")
    empty_password = os.getenv("EMPTY_PASSWORD")
    
    login_page.enter_login_name(empty_login_name)
    login_page.enter_password(empty_password)
    login_page.click_login_button()
    
    login_page.assert_error_displayed()

    print("Login with empty credentials displayed error as expected.")

@pytest.mark.smoke
@pytest.mark.p1
def test_forgot_password_link_navigates_correctly(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    
    login_page.click_forgot_password_link()
    
    # Verify navigation by checking URL
    page.wait_for_url("**/forgotten/**")
    assert "forgotten" in page.url, "Did not navigate to Forgot Password page"

    print("Forgot Password link navigated correctly.")

