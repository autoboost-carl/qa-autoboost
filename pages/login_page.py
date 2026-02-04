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
    def welcome_menu_link(self):
        # "Welcome back ..." top link (sometimes appears in top menu)
        return self.page.locator("a").filter(has_text=re.compile(r"Welcome back", re.IGNORECASE)).first
    
    @property
    def logout_menu_hover(self):
        # The actual logout option: "Not {user}? Logoff"
        return self.page.locator("a").filter(
            has_text=re.compile(r"Not .*\\? Logoff", re.IGNORECASE)
        ).first

    @property
    def logout_link(self):
        # Logout link typically contains account/logout
        return self.page.locator("a[href*='account/logout']").first

    @property
    def logged_off_message(self):
        return self.page.locator("text=You have been logged off your account.")
    
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
        self.wait_for_load_state()
    
    def logout(self) -> None:
        """Logout via hover menu and verify logged-off confirmation."""
        # Hover over the welcome/account dropdown
        expect(self.welcome_menu_link).to_be_visible(timeout=10_000)
        self.hover_over_element(self.welcome_menu_link)

        # Wait for logout option to appear and click it
        expect(self.logout_menu_hover).to_be_visible(timeout=10_000)
        self.click_element(self.logout_menu_hover)

        # Assert logged off confirmation
        expect(self.logged_off_message).to_be_visible(timeout=10_000)
    
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
    
    


