from playwright.sync_api import Page, expect
from pages.base.base_page import BasePage
import re

class LoginPage(BasePage):
    def __init__(self, page: Page):
        # Initialize the base page with the provided Page object
        super().__init__(page)
        self.url = "https://automationteststore.com/index.php?rt=account/login"
    
    # ==========================================
    # Locators
    # ==========================================

    @property
    def login_name_input(self):
        return self.page.locator("input[name='loginname']")
    
    @property
    def password_input(self):
        return self.page.locator("input[name='password']")
    
    @property
    def login_button(self):
        return self.page.locator("button:has-text('Login')")
    
    @property
    def forgot_password_link(self):
        return self.page.locator("a:has-text('Forgot your password')")
    
    @property
    def error_message(self):
        return self.page.get_by_text("Error: Incorrect login or password provided.")
    
    @property
    def success_message(self):
        return self.page.locator("//*[contains(text(), 'Welcome back')]")
    
    @property
    def logout_link(self):
        return self.page.locator("a[href*='account/logout']")
    
    # ==========================================
    # Actions - Login
    # ==========================================
    def navigate_to_login(self):
        self.navigate(self.url)

        # Explicit ready signal: username input visible
        self.wait_for_element(self.login_name_input)
    
    def enter_login_name(self, login_name: str) -> None:
        self.fill_input(self.login_name_input, login_name)
    
    def enter_password(self, password: str) -> None:
        self.fill_input(self.password_input, password)
    
    def click_login_button(self) -> None:
        self.click_element(self.login_button)
    
    def click_forgot_password_link(self) -> None:
        self.click_element(self.forgot_password_link)
    
    
    # ==========================================
    # High-Level Methods
    # ==========================================
    def login(self, login_name: str, password: str) -> None:
        """Full login process."""
        # Make sure we're on login page
        expect(self.page).to_have_url(re.compile(r"rt=account/login"), timeout=10_000)

        self.enter_login_name(login_name)
        self.enter_password(password)
        self.click_login_button()
        
        # Success is typically account page or welcome text.
        try:
            expect(self.page).to_have_url(re.compile(r"rt=account/account"), timeout=10_000)
        except Exception:
            # If not redirected, an error message should appear
            expect(self.error_message).to_be_visible(timeout=10_000)
    
    def logout(self) -> None:
        """Logout from the account by navigating to logout URL."""
        # If you have a visible logout link, use it; otherwise navigate.
        if self.logout_link.is_visible(timeout=1500):
            self.click_element(self.logout_link)
        else:
            self.navigate("https://automationteststore.com/index.php?rt=account/logout")

        # Verify we are no longer on account page (login page or logout success page)
        expect(self.page).to_have_url(re.compile(r"rt=account/(logout|login)"), timeout=10_000)
    
    # ==========================================
    # Verifications
    # ==========================================
    def is_error_displayed(self) -> bool:
        return self.error_message.is_visible()
    
    def is_success_message_displayed(self) -> bool:
        return self.success_message.is_visible()

    # ==========================================
    # Assertions
    # ==========================================
    # Login with valid credentials
    def assert_login_successful(self, expected_login_text: str | None = None) -> None:
        # Prefer URL-based confirmation; welcome text can vary
        expect(self.page).to_have_url(re.compile(r"rt=account/account"), timeout=10_000)
        if expected_login_text:
            self.assert_text_contains(self.success_message, expected_login_text)

    # Login with invalid credentials
    def assert_error_displayed(self, expected_error_message: str | None = None) -> None:
        self.assert_element_visible(self.error_message)
        if expected_error_message:
            self.assert_text_contains(self.error_message, expected_error_message)
    
    


