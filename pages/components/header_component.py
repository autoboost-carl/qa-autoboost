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
    def search_results_header(self):
        return self.page.locator("h4").filter(has_text="Products meeting the search criteria")
    
    @property
    def product_names(self):
        return self.page.locator("a.prdocutname, a.productname")
    
    #==========================================
    # Locators - Navigation Links & Method for Category Links
    #==========================================

    @property
    def main_navigation_links(self):
        return self.page.locator("nav.subnav ul.nav-pills")
    
    @property
    def home_link(self):
        return self.page.locator("nav.subnav ul.nav-pills >> text=Home")
    
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
        self.click_element(self.logo)
        # Clicking should take you home and you should at least see the search input
        self.wait_for_element(self.search_input)
    
    def search_product_with_button(self, product_name: str) -> None:
        self.fill_input(self.search_input, product_name)
        self.click_element(self.search_button)
        # Explicit wait for results header
        expect(self.search_results_header).to_be_visible(timeout=10000)
    
    def search_product_with_key(self, product_name: str) -> None:
        self.fill_input(self.search_input, product_name)
        self.search_input.press("Enter")
        self.wait_for_load_state()
    
    
    def navigate_to_category(self, category_name: str) -> None:
        category_link = self.get_category_link(category_name)
        self.click_element(category_link)
        # Wait for something stable on category page (products grid exists)
        expect(self.product_names.first).to_be_visible(timeout=10000)
    
    def click_home_link(self) -> None:
        self.click_element(self.home_link)
        self.wait_for_element(self.search_input)
    
    #==========================================
    # Actions - Shopping Cart
    #==========================================
    def go_to_cart(self) -> None:
        self.click_element(self.cart_link)
        # Expect it has h1 "Shopping Cart"
        expect(self.page.locator("h1")).to_contain_text("Shopping Cart", timeout=10000)
    
    #==========================================
    # Verifications
    #==========================================
    def is_user_logged_in(self) -> bool:
        return self.is_visible(self.account_menu_link)
    
    def get_cart_item_count_text(self) -> str:
        return self.get_text(self.cart_item_count)
    
    def is_logo_displayed(self) -> bool:
        return self.is_visible(self.logo)

    def is_search_input_displayed(self) -> bool:
        return self.is_visible(self.search_input)
    
    
    #==========================================
    # Assertions
    #=========================================

    def assert_header_visible(self) -> None:
        self.assert_element_visible(self.logo)
        self.assert_element_visible(self.search_input)
        self.assert_element_visible(self.search_button)
        self.assert_element_visible(self.main_navigation_links)

    def assert_user_logged_in(self) -> None:
        expect(self.account_menu_link).to_be_visible(timeout=10000)
    
    def assert_cart_item_count(self, expected_count: str) -> None:
        expect(self.cart_item_count).to_have_text(expected_count, timeout=10000)
    
    def assert_search_results(self, search_term: str) -> None:
        # Results header visible
        expect(self.search_results_header).to_be_visible(timeout=10000)

        # Search term echoed in results input (wait until it contains term)
        expect(self.search_input_results).to_have_value(re.compile(re.escape(search_term), re.IGNORECASE), timeout=10000)

        # At least one product visible
        expect(self.product_names.first).to_be_visible(timeout=10000)

        # At least one product title contains the term (case-insensitive)
        titles = self.product_names.all_inner_texts()
        match_found = any(search_term.lower() in t.lower() for t in titles)

        assert match_found, (
            f"No product titles contained the search term '{search_term}'.\n"
            f"Products found: {titles}"
        )


    

        
    
