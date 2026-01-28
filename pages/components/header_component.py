from playwright.sync_api import Page, expect
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
        return self.page.locator("a.logo")
    
    @property
    def search_input(self):
        return self.page.locator("input[name='filter_keyword']")
    
    @property
    def search_input_results(self):
        return self.page.locator("input[name='keyword']")
    
    @property
    def search_button(self):
        return self.page.locator("i.fa-search")
    
    @property
    def search_results(self):
        return self.page.locator("h4").filter(has_text="Products meeting the search criteria")
    
    @property
    def product_names(self):
        return self.page.locator("a.prdocutname")
    
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
    
    def search_product_with_button(self, product_name: str) -> None:
        expect(self.search_input).to_be_visible()
        self.search_input.fill(product_name)
        self.search_button.click()
        self.wait_for_load_state("networkidle")
    
    def search_product_with_key(self, product_name: str) -> None:
        expect(self.search_input).to_be_visible()
        self.search_input.fill(product_name)
        self.search_input.press("Enter")
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
        self.assert_element_visible(self.logo)
        self.assert_element_visible(self.search_input)
        self.assert_element_visible(self.search_button)
        self.assert_element_visible(self.main_navigation_links)

    def assert_user_logged_in(self) -> None:
        assert self.is_user_logged_in(), "User is not logged in, but expected to be logged in."
    
    def assert_cart_item_count(self, expected_count: str) -> None:
        actual_count = self.get_cart_item_count_text()
        assert actual_count == expected_count, f"Expected cart item count to be '{expected_count}', but got '{actual_count}'."
    
    def assert_search_results(self, search_term: str) -> None:
        # Search term echoed in input
        search_value = self.search_input_results.input_value()
        assert search_term.lower() in search_value.lower(), (
            f"Expected search term '{search_term}' to be present in search input, "
            f"but got '{search_value}'"
        )

        # Product exists
        product_count = self.product_names.count()
        assert product_count > 0, "No products were displayed in search results"

        # At least one product name contains the search term
        product_titles = self.product_names.all_inner_texts()
        match_found = any(
            search_term.lower() in title.lower()
            for title in product_titles
        )

        assert match_found, (
            f"No product titles contained the search term '{search_term}'.\n"
            f"Products found: {product_titles}"
        )


    

        
    
