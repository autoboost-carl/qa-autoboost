from playwright.sync_api import Page
from pages.base.base_page import BasePage

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
        return self.page.get_by_role("input", name="loginname")
    
    @property
    def password_input(self):
        return self.page.get_by_role("input", name="password")
    
    @property
    def login_button(self):
        return self.page.get_by_role("button", title="Login")
    
    @property
    def forgot_password_link(self):
        return self.page.get_by_role("link", name="Forgot your password?")
    
    @property
    def error_message(self):
        return self.page.get_by_text("Error: Incorrect login or password provided.")
    
    @property
    def success_message(self):
        return self.page.locator("//*[contains(text(), 'Welcome back')]")
    
    # ==========================================
    # Actions
    # ==========================================
    def navigate_to_login(self):
        self.navigate(self.url)

        # Wait for the page to be fully loaded
        self.wait_for_load_state("networkidle")
    
    def enter_login_name(self, login_name: str) -> None:
        self.login_name_input.fill(login_name)
    
    def enter_password(self, password: str) -> None:
        self.password_input.fill(password)
    
    def click_login_button(self) -> None:
        self.login_button.click()
    
    def click_forgot_password_link(self) -> None:
        self.forgot_password_link.click()
    
    # ==========================================
    # High-Level Methods
    # ==========================================
    def login(self, login_name: str, password: str) -> None:
        """Full login process."""
        self.enter_login_name(login_name)
        self.enter_password(password)
        self.click_login_button()
        self.wait_for_load_state("networkidle")
    
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
    def assert_login_successful(self, expected_login_text: str = None) -> None:
        self.is_success_message_displayed()
        if expected_login_text:
            self.assert_text_contains(self.success_message, expected_login_text)

    # Login with invalid credentials
    def assert_error_displayed(self, expected_error_message: str = None) -> None:
        self.is_error_displayed()
        if expected_error_message:
            self.assert_text_contains(self.error_message, expected_error_message)
    
    


