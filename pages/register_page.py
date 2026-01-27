from playwright.sync_api import Page
from pages.base.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://automationteststore.com/index.php?rt=account/create"
    
    # ==========================================
    # Locators - Personal Information
    # ==========================================

    @property
    def first_name_input(self):
        return self.page.locator("input[name='firstname']")
    
    @property
    def last_name_input(self):
        return self.page.locator("input[name='lastname']")
    
    @property
    def email_input(self):
        return self.page.locator("input#AccountFrm_email")
    
    @property
    def telephone_input(self):
        return self.page.locator("input[name='telephone']")
    
    @property
    def fax_input(self):
        return self.page.locator("input[name='fax']")
    
    # ==========================================
    # Locators - Address Information
    # ==========================================

    @property
    def company_input(self):
        return self.page.locator("input[name='company']")
    
    @property
    def address_1_input(self):
        return self.page.locator("input[name='address_1']")
    
    @property
    def address_2_input(self):
        return self.page.locator("input[name='address_2']")
    
    @property
    def city_input(self):
        return self.page.locator("input[name='city']")
    
    @property
    def region_dropdown(self):
        return self.page.locator("select[name='zone_id']")
    
    @property
    def zipcode_input(self):
        return self.page.locator("input[name='postcode']")
    
    @property
    def country_dropdown(self):
        return self.page.locator("select[name='country_id']")
    
    # ==========================================
    # Locators - Login Information
    # ==========================================

    @property
    def login_name_input(self):
        return self.page.locator("input[name='loginname']")
    
    @property
    def password_input(self):
        return self.page.locator("input[name='password']")
    
    @property
    def confirm_password_input(self):
        return self.page.locator("input[name='confirm']")
    
    # ==========================================
    # Locators - Newsletter & Privacy
    # ==========================================

    @property
    def newsletter_yes_radio(self):
        return self.page.locator("input[name='newsletter'][value='1']")
    
    @property
    def newsletter_no_radio(self):
        return self.page.locator("input[name='newsletter'][value='0']")
    
    @property
    def privacy_policy_checkbox(self):
        return self.page.locator("input[name='agree']")
    
    # ==========================================
    # Locators - Buttons & Messages
    # ==========================================

    @property
    def continue_button(self):
        return self.page.locator("button:has-text('Continue')")
    
    @property
    def page_heading(self):
        return self.page.locator("h1:has-text('Create Account')")
    
    @property
    def success_message(self):
        return self.page.locator("span.maintext:has-text('Your Account Has Been Created!')")
    
    @property
    def error_message(self):
        return self.page.locator("div.alert.alert-danger")
    
    
    # ==========================================
    # Actions - Personal & Address Information
    # ==========================================
    def navigate_to_register(self):
        self.navigate(self.url)
        self.wait_for_load_state("networkidle")
    
    def enter_first_name(self, first_name: str) -> None:
        self.first_name_input.fill(first_name)
    
    def enter_last_name(self, last_name: str) -> None:
        self.last_name_input.fill(last_name)
    
    def enter_email(self, email: str) -> None:
        self.email_input.fill(email)
    
    def enter_telephone(self, telephone: str) -> None:
        self.telephone_input.fill(telephone)
    
    def enter_fax(self, fax: str) -> None:
        self.fax_input.fill(fax)
    
    def enter_company(self, company: str) -> None:
        self.company_input.fill(company)
    
    def enter_address_1(self, address_1: str) -> None:
        self.address_1_input.fill(address_1)
    
    def enter_address_2(self, address_2: str) -> None:
        self.address_2_input.fill(address_2)
    
    def enter_city(self, city: str) -> None:
        self.city_input.fill(city)
    
    def select_region(self, region: str) -> None:
        self.region_dropdown.select_option(region)
    
    def enter_zipcode(self, zipcode: str) -> None:
        self.zipcode_input.fill(zipcode)
    
    def select_country(self, country: str) -> None:
        self.country_dropdown.select_option(country)
    
    # ==========================================
    # Actions - Login Information
    # ==========================================
    
    def enter_login_name(self, login_name: str) -> None:
        self.login_name_input.fill(login_name)
    
    def enter_password(self, password: str) -> None:
        self.password_input.fill(password)
    
    def enter_confirm_password(self, confirm_password: str) -> None:
        self.confirm_password_input.fill(confirm_password)
    
    # ==========================================
    # Actions - Newsletter & Privacy
    # ==========================================

    def select_newsletter_subscription(self, subscribe: bool) -> None:
        if subscribe:
            self.newsletter_yes_radio.check()
        else:
            self.newsletter_no_radio.check()
    
    def agree_to_privacy_policy(self) -> None:
        self.privacy_policy_checkbox.check()

    def click_continue_button(self) -> None:
        self.continue_button.click()
    
    # ==========================================
    # Full Registration Process
    # ==========================================

    def register_user(self, user_data: dict) -> None:
        """Full user registration process."""
        # Personal Information
        self.enter_first_name(user_data["first_name"])
        self.enter_last_name(user_data["last_name"])
        self.enter_email(user_data["email"])
        self.enter_telephone(user_data["telephone"])
        # Optional fields for personal information
        if user_data.get("fax"):
            self.enter_fax(user_data["fax"])
        if user_data.get("company"):
            self.enter_company(user_data["company"])
        
        # Address Information
        self.enter_address_1(user_data["address_1"])
        # Optional address field
        if user_data.get("address_2"):
            self.enter_address_2(user_data["address_2"])
        self.enter_city(user_data["city"])

        # Select country first to load regions
        self.select_country(user_data["country"])
        self.page.wait_for_timeout(3000)  # Wait for regions to load
        self.select_region(user_data["region"])
        self.enter_zipcode(user_data["zipcode"])

        # Login Information
        self.enter_login_name(user_data["login_name"])
        self.enter_password(user_data["password"])
        self.enter_confirm_password(user_data["password"])
        
        # Newsletter & Privacy
        # Must be true or false
        if user_data.get("newsletter", False):
            self.select_newsletter_subscription(True)
        else:
            self.select_newsletter_subscription(False)
        
        # Privacy Policy (Mandatory)
        self.agree_to_privacy_policy()

        # Submit Registration
        self.click_continue_button()
    
    # ==========================================
    # Verification Methods
    # ==========================================

    def is_registration_successful(self) -> bool:
        """Check if registration was successful."""
        self.wait_for_load_state("networkidle")
        return self.success_message.is_visible()

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed."""
        return self.error_message.is_visible()
    
    def get_error_message_text(self) -> str:
        """Get the text of the error message."""
        if self.is_error_displayed():
            return self.get_text(self.error_message)
        return ""
    
    # ==========================================
    # Assertion Methods
    # ==========================================
    def assert_registration_successful(self) -> None:
        """Assert that registration was successful."""
        self.assert_element_visible(self.success_message)
    
    def assert_error_displayed(self) -> None:
        """Assert that an error message is displayed."""
        self.assert_element_visible(self.error_message)
    
    def assert_privacy_policy_error_displayed(self) -> None:
        """Assert that privacy policy error is displayed."""
        self.assert_element_visible(self.error_message)
    
    def logout(self) -> None:
        """Logout from the account by navigating to logout URL."""
        self.navigate("https://automationteststore.com/index.php?rt=account/logout")