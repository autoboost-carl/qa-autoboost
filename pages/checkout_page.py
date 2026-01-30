from playwright.sync_api import Page
from pages.base.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.footer_component import FooterComponent

class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Checkout URL
        self.url = "https://automationteststore.com/index.php?rt=checkout/checkout"
        
        # Reusable components
        self.header = HeaderComponent(page)
        self.footer = FooterComponent(page)
    
    #=====================================
    # Locators - Checkout Options
    #=====================================
    
    @property
    def guest_checkout_option(self):
        """Radio button for guest checkout"""
        return self.page.locator("input[name='account'][value='guest']")
    
    @property
    def register_checkout_option(self):
        """Radio button for register during checkout"""
        return self.page.locator("input[name='account'][value='register']")
    
    @property
    def login_checkout_option(self):
        """Radio button for login during checkout"""
        return self.page.locator("input[name='account'][value='login']")
    
    #=====================================
    # Locators - Guest Checkout Form
    #=====================================
    
    @property
    def guest_email_input(self):
        return self.page.locator("input#guestFrm_email")
    
    @property
    def guest_firstname_input(self):
        return self.page.locator("input#guestFrm_firstname")
    
    @property
    def guest_lastname_input(self):
        return self.page.locator("input#guestFrm_lastname")
    
    @property
    def guest_address_input(self):
        return self.page.locator("input#guestFrm_address_1")
    
    @property
    def guest_city_input(self):
        return self.page.locator("input#guestFrm_city")
    
    @property
    def guest_zipcode_input(self):
        return self.page.locator("input#guestFrm_postcode")
    
    @property
    def guest_state_select(self):
        return self.page.locator("select#guestFrm_zone_id")
    
    @property
    def guest_country_select(self):
        return self.page.locator("select#guestFrm_country_id")
    
    @property
    def guest_phone_input(self):
        return self.page.locator("input#guestFrm_telephone")
    
    #=====================================
    # Locators - Login Form
    #=====================================
    
    @property
    def login_email_input(self):
        return self.page.locator("input[name='login_name']")
    
    @property
    def login_password_input(self):
        return self.page.locator("input[name='password']")
    
    @property
    def login_submit_button(self):
        return self.page.locator("button:has-text('Login')")
    
    
    #=====================================
    # Locators - Confirmation
    #=====================================
    
    @property
    def confirm_order_button(self):
        return self.page.locator("button:has-text('Confirm Order')")
    
    @property
    def continue_button(self):
        return self.page.locator("button:has-text('Continue')")
    
    @property
    def order_confirmation_message(self):
        return self.page.locator("h1:has-text('Your Order Has Been Processed!')")
    
    
    #=====================================
    # Actions - Navigation
    #=====================================
    
    def navigate_to_checkout(self) -> None:
        self.navigate(self.url)
        self.wait_for_load_state("networkidle")
    
    #=====================================
    # Actions - Guest Checkout
    #=====================================
    
    def select_guest_checkout(self) -> None:
        """Select guest checkout option and continue"""
        self.guest_checkout_option.click()
        self.page.wait_for_timeout(500)
        
        # After selecting guest, look for a continue/checkout button
        # Try to find and click a button that proceeds with guest checkout
        continue_buttons = [
            self.page.locator("button:has-text('Continue')").first,
            self.page.locator("button:has-text('Checkout')").first,
            self.page.locator("button[type='submit']").first,
            self.page.locator("input[type='submit']").first,
        ]
        
        for button in continue_buttons:
            try:
                if button.is_visible():
                    button.click()
                    self.wait_for_load_state("networkidle")
                    return
            except:
                pass
    
    def fill_guest_information(self, email: str, firstname: str, lastname: str, 
                               address: str, city: str, zipcode: str, 
                               phone: str, country: str = "United States", 
                               state: str = "California") -> None:
        """Fill all guest information fields"""
        self.guest_email_input.fill(email)
        self.guest_firstname_input.fill(firstname)
        self.guest_lastname_input.fill(lastname)
        self.guest_address_input.fill(address)
        self.guest_city_input.fill(city)
        self.guest_zipcode_input.fill(zipcode)
        self.guest_phone_input.fill(phone)
        
        # Select country
        self.guest_country_select.select_option(country)
        
        # Select state
        self.guest_state_select.select_option(state)
        
        # After filling guest info, click continue/checkout button to proceed to shipping/payment
        self.page.wait_for_timeout(500)
        continue_buttons = [
            self.page.locator("button:has-text('Continue')").first,
            self.page.locator("button:has-text('Next')").first,
            self.page.locator("button:has-text('Checkout')").first,
            self.page.locator("input[type='submit'][value*='Continue']").first,
            self.page.locator("input[type='submit'][value*='Next']").first,
            self.page.locator("button[type='submit']").first,
            self.page.locator("input[type='submit']").first,
        ]
        
        for button in continue_buttons:
            try:
                if button.is_visible(timeout=2000):
                    button.click()
                    self.wait_for_load_state("networkidle")
                    return
            except:
                pass
    
    #=====================================
    # Actions - Login Checkout
    #=====================================
    
    def select_login_checkout(self) -> None:
        """Select login checkout option"""
        self.login_checkout_option.click()
        self.wait_for_load_state("networkidle")
    
    def login_during_checkout(self, email: str, password: str) -> None:
        """Login during checkout process"""
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_submit_button.click()
        self.wait_for_load_state("networkidle")
    
    #=====================================
    # Actions - Order Confirmation
    #=====================================
    
    def confirm_order(self) -> None:
        """Click confirm order button"""
        self.confirm_order_button.click()
        self.wait_for_load_state("networkidle")
    
    #=====================================
    # Verifications
    #=====================================
    
    def is_on_checkout_page(self) -> bool:
        """Verify if on checkout page (includes login page that shows guest checkout option)"""
        # Check URL contains checkout or login (since guest option appears on login page during checkout)
        url_check = ("checkout" in self.page.url.lower() or "login" in self.page.url.lower())
        
        # Try to find any checkout-related element visible
        try:
            # Check for guest option, login option, or any checkout form element
            any_checkout_element = (
                self.guest_checkout_option.is_visible() or
                self.login_checkout_option.is_visible() or
                self.guest_email_input.is_visible() or
                self.login_email_input.is_visible()
            )
            return url_check and any_checkout_element
        except:
            # Fallback: just check for guest option
            try:
                return self.guest_checkout_option.is_visible()
            except:
                return url_check
    
    def is_order_confirmed(self) -> bool:
        """Verify if order was successfully confirmed"""
        return self.order_confirmation_message.is_visible()
    
    def wait_for_order_confirmation(self, timeout: int = 30000) -> None:
        """Wait for order confirmation message to appear"""
        self.order_confirmation_message.wait_for(state="visible", timeout=timeout)
    
    #=====================================
    # Assertions
    #=====================================
    
    def assert_on_checkout_page(self) -> None:
        """Assert that we are on the checkout page"""
        try:
            assert self.is_on_checkout_page(), \
                f"Not on the Checkout Page. Current URL: {self.page.url}"
        except AssertionError as e:
            print(f"DEBUG: {str(e)}")
            print(f"DEBUG: Page title: {self.page.title()}")
            print(f"DEBUG: Guest option visible: {self.guest_checkout_option.is_visible() if 'guest_checkout_option' in dir(self) else 'N/A'}")
            raise
    
    def assert_order_confirmed(self) -> None:
        assert self.is_order_confirmed(), "Order confirmation message not visible."