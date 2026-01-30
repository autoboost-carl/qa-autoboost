import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@allure.feature("Login UI")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_login_page_elements_visible(page: Page):
    login_page = LoginPage(page)

    with allure.step("Navigate to login"):
        login_page.navigate_to_login()
    with allure.step("Assert login input, password input, login button and forgot password link are visible"):
        assert login_page.login_name_input.is_visible(), "Login name input is not visible"
        assert login_page.password_input.is_visible(), "Password input is not visible"
        assert login_page.login_button.is_visible(), "Login button is not visible"
        assert login_page.forgot_password_link.is_visible(), "Forgot password link is not visible"

    print("All login page elements are visible.")

@allure.feature("Login Flow")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_login_with_valid_credentials(page: Page):
    login_page = LoginPage(page)

    with allure.step("Navigate to login"):
        login_page.navigate_to_login()
    
    valid_login_name = os.getenv("VALID_LOGIN_NAME")
    valid_password = os.getenv("VALID_PASSWORD")

    with allure.step("Enter valid credentials and login"):
        login_page.enter_login_name(valid_login_name)
        login_page.enter_password(valid_password)
        login_page.click_login_button()

    with allure.step("Assert login was successful"):
        login_page.assert_login_successful()

    print("Login with valid credentials successful.")

@allure.feature("Login Flow")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_login_with_invalid_credentials(page: Page):
    login_page = LoginPage(page)

    with allure.step("Navigate to login"):
        login_page.navigate_to_login()
    
    invalid_login_name = os.getenv("INVALID_LOGIN_NAME")
    invalid_password = os.getenv("INVALID_PASSWORD")
    
    with allure.step("Enter invalid credentials and login"):
        login_page.enter_login_name(invalid_login_name)
        login_page.enter_password(invalid_password)
        login_page.click_login_button()
    
    with allure.step("Assert an error was displayed and login was not successful"):
        login_page.assert_error_displayed()

    print("Login with invalid credentials displayed error as expected.")

@allure.feature("Login Flow")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_login_with_empty_credentials(page: Page):
    login_page = LoginPage(page)

    with allure.step("Navigate to login"):
        login_page.navigate_to_login()
    
    empty_login_name = os.getenv("EMPTY_LOGIN_NAME")
    empty_password = os.getenv("EMPTY_PASSWORD")
    
    with allure.step("Leave login name and password blank"):
        login_page.enter_login_name(empty_login_name)
        login_page.enter_password(empty_password)
        login_page.click_login_button()
    
    with allure.step("Assert an error was displayed and login was not successful"):
        login_page.assert_error_displayed()

    print("Login with empty credentials displayed error as expected.")

@allure.feature("Forgot Password link")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_forgot_password_link_navigates_correctly(page: Page):
    login_page = LoginPage(page)

    with allure.step("Navigate to login"):
        login_page.navigate_to_login()
    
    with allure.step("Click on Forgot password and assert that it's navigating to the right page"):
        login_page.click_forgot_password_link()
    
        # Verify navigation by checking URL
        page.wait_for_url("**/forgotten/**")
        assert "forgotten" in page.url, "Did not navigate to Forgot Password page"

    print("Forgot Password link navigated correctly.")

