from playwright.sync_api import Page
from pages.base.base_page import BasePage

class FooterComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    #==========================================
    # Locators - Footer Links
    #==========================================    

    @property
    def about_us_link(self):
        return self.page.locator("footer a:has-text('About Us')")
    
    @property
    def contact_us_link(self):
        return self.page.locator("footer a:has-text('Contact Us')")
    
    @property
    def privacy_policy_link(self):
        return self.page.locator("footer a:has-text('Privacy Policy')")
    
    #==========================================
    # Locators - Contact Form
    #==========================================
    @property
    def contact_firstname_input(self):
        firstname = self.page.locator("input#ContactUsFrm_first_name")
        return firstname
    
    @property
    def contact_email_input(self):
        return self.page.locator("input#ContactUsFrm_email")
    
    @property
    def contact_enquiry_textarea(self):
        return self.page.locator("textarea#ContactUsFrm_enquiry")
   
    #==========================================
    # Locators - Buttons and Success Message
    #==========================================
    @property
    def continue_about_us(self):
        return self.page.locator("button:has-text('Continue')")
    
    @property
    def continue_privacy_policy(self):
        return self.page.locator("button:has-text('Continue')")
    
    @property
    def submit_inquiry(self):
        return self.page.locator("button:has-text('Submit')")
    
    @property
    def success_message(self):
        return self.page.locator("//*[contains(text(), 'sent to the store owner')]")

    #==========================================
    # Actions - Footer Links
    #==========================================
    def click_about_us(self) -> None:
        self.click_element(self.about_us_link)

    def click_contact_us(self) -> None:
        self.click_element(self.contact_us_link)
        # contact form should be visible
        self.wait_for_element(self.contact_firstname_input)

    def click_privacy_policy(self) -> None:
        self.click_element(self.privacy_policy_link)
    
    #==========================================
    # Actions - Contact Form
    #==========================================
    def fill_and_submit_contact_form(self, firstname: str, email: str, enquiry: str) -> None:
        """Fill out and submit the contact us form"""
        self.fill_input(self.contact_firstname_input, firstname)
        self.fill_input(self.contact_email_input, email)
        self.fill_input(self.contact_enquiry_textarea, enquiry)

        self.click_element(self.submit_inquiry)

        self.wait_for_element(self.success_message)
    
    #==========================================
    # Actions - Scroll to Footer
    #==========================================
    def scroll_to_footer(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.wait_for_element(self.contact_us_link)
    
    #==========================================
    # Verifications - Footer Links
    #==========================================
    def is_about_us_visible(self) -> bool:
        return self.is_visible(self.about_us_link)
    
    def is_contact_us_visible(self) -> bool:
        return self.is_visible(self.contact_us_link)
    
    def is_privacy_policy_visible(self) -> bool:
        return self.is_visible(self.privacy_policy_link)
    
    def is_success_message_displayed(self) -> bool:
        return self.is_visible(self.success_message)
    
    #==========================================
    # Assertions - Footer Links
    #==========================================
    def assert_footer_links_visible(self) -> None:
        self.assert_element_visible(self.about_us_link)
        self.assert_element_visible(self.privacy_policy_link)
        self.assert_element_visible(self.contact_us_link)
    
    def assert_successful_contact_us(self, expected_contact_us_text: str | None = None) -> None:
        self.assert_element_visible(self.success_message)
        if expected_contact_us_text:
            self.assert_text_contains(self.success_message, expected_contact_us_text)
    
    
