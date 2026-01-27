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
    # Actions - Footer Links
    #==========================================
    def click_about_us(self) -> None:
        self.about_us_link.click()

    def click_contact_us(self) -> None:
        self.contact_us_link.click()

    def click_privacy_policy(self) -> None:
        self.privacy_policy_link.click()
    
    
    #==========================================
    # Actions - Scroll to Footer
    #==========================================
    def scroll_to_footer(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.wait_for_load_state("networkidle")
    
    #==========================================
    # Verifications - Footer Links
    #==========================================
    def is_about_us_visible(self) -> bool:
        return self.about_us_link.is_visible()
    
    def is_contact_us_visible(self) -> bool:
        return self.contact_us_link.is_visible()
    
    def is_privacy_policy_visible(self) -> bool:
        return self.privacy_policy_link.is_visible()
    
    #==========================================
    # Assertions - Footer Links
    #==========================================
    def assert_footer_links_visible(self) -> None:
        self.assert_element_visible(self.about_us_link, "About us")
        self.assert_element_visible(self.privacy_policy_link, "Privacy Link")
        self.assert_element_visible(self.contact_us_link, "Contact Us")
    
    
