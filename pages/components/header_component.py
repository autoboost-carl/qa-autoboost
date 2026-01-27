from playwright.sync_api import Page
from pages.base.base_page import BasePage
import re

class HeaderComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    #==========================================
    # Locators - Logo & Search
    #==========================================    
    
    @property
    def logo(self):
        return self.page.locator("div#logo a")
    
    @property
    def search_input(self):
        return self.page.locator("input[name='filter_keyword']")
    
    @property
    def search_button(self):
        return self.page.locator("div.button-in-input i.fa-search")
    
    #==========================================
    # Locators - Navigation Links
    #==========================================

    @property
    def main_navigation_links(self):
        return self.page.locator("nav.subnav ul.nav-pills")
    
    @property
    def home_link(self):
        return self.page.locator("nav.subnav ul.nav-pills >> text=Home")
    
    @property
    def get_category_link(self, category_name: str):
        return self.page.get_by_role("link", name=re.compile(f"^{category_name}$", re.IGNORECASE))
    
    @property
    def account_menu_link(self):
        return self.page.locator("ul.nav.topcart a[href*='account/account']")
    
    #==========================================
    # Locators - Cart
    #==========================================

    @property
    def cart_link(self):
        return self.page.locator("ul.nav.topcart a[href*='checkout/cart']")
    
    @property
    def cart_item_count(self):
        return self.page.locator("ul.nav.topcart span.label")
    
    #==========================================
    # Actions - Navigation Links
    #==========================================
    def click_logo(self) -> None:
        self.logo.click()
        self.wait_for_load_state("networkidle")
    
    def search_product(self, product_name: str) -> None:
        self.search_input.fill(product_name)
        self.search_button.click()
        self.wait_for_load_state("networkidle")
    
    def navigate_to_category(self, category_name: str) -> None:
        category_link = self.get_category_link(category_name)
        category_link.click()
        self.wait_for_load_state("networkidle")
    
    def click_home_link(self) -> None:
        self.home_link.click()
        self.wait_for_load_state("networkidle")
    
    #==========================================
    # Actions - Shopping Cart
    #==========================================
    def go_to_cart(self) -> None:
        self.cart_link.click()
        self.wait_for_load_state("networkidle")
    
    #==========================================
    # Verifications
    #==========================================
    def is_user_logged_in(self) -> bool:
        return self.account_menu_link.is_visible()
    
    def get_cart_item_count_text(self) -> str:
        return self.get_text(self.cart_item_count)
    
    def is_logo_displayed(self) -> bool:
        return self.logo.is_visible()

    def is_search_input_displayed(self) -> bool:
        return self.search_input.is_visible()
    
    #==========================================
    # Assertions
    #=========================================

    def assert_header_visible(self) -> None:
        self.assert_element_visible(self.logo, "Logo")
        self.assert_element_visible(self.search_input, "Search Input")
        self.assert_element_visible(self.search_button, "Search Button")
        self.assert_element_visible(self.main_navigation_links, "Main Navigation Links")

    def assert_user_logged_in(self) -> None:
        assert self.is_user_logged_in(), "User is not logged in, but expected to be logged in."
    
    def assert_cart_item_count(self, expected_count: str) -> None:
        actual_count = self.get_cart_item_count_text()
        assert actual_count == expected_count, f"Expected cart item count to be '{expected_count}', but got '{actual_count}'."
    

        
    
