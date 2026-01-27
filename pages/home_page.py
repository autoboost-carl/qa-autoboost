from playwright.sync_api import Page
from pages.base.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.footer_component import FooterComponent
import re

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://automationteststore.com/"
        self.header = HeaderComponent(page)
        self.footer = FooterComponent(page)
    
    # ==========================================
    # Locators
    # ==========================================

    @property
    def main_banner(self):
        return self.page.locator("div.banner-container")
    
    @property
    def featured_products_section(self):
        return self.page.locator("section.promo_block")
    
    @property
    def all_product_cards(self):
        return self.page.locator("div.thumbnails div.col-md-3")
    
    @property
    def get_product_by_name(self, product_name: str):
        return self.page.get_by_role("link", name=re.compile(f"^{product_name}$", re.IGNORECASE))

    # ==========================================
    # Actions - Home Page
    # ==========================================
    def navigate_to_home(self):
        self.navigate(self.url)

        # Wait for the page to be fully loaded
        self.wait_for_load_state("networkidle")
    
    def click_product(self, product_name: str) -> None:
        self.get_product_by_name(product_name).click()
        self.wait_for_load_state("networkidle")
    
    # ==========================================
    # Verifications - Home Page
    # ==========================================
    def is_on_home_page(self) -> bool:
        """Verify if the current page is the home page by checking the URL and main banner visibility."""
        url_check = self.page.url == self.url
        banner_visible = self.main_banner.is_visible()
        return url_check and banner_visible
    
    def get_product_count(self) -> int:
        """Obtain the count of all product cards displayed on the home page."""
        return self.all_product_cards.count()

    def is_product_visible(self, product_name: str) -> bool:
        """Check if a specific product is visible on the home page."""
        product = self.get_product_by_name(product_name)
        return product.is_visible()
    
    # ==========================================
    # Assertions - Home Page
    # ==========================================
    def assert_on_home_page(self) -> None:
        assert self.is_on_home_page(), "Not on the Home Page."

        # Also assert header and footer components are visible
        assert self.header.assert_header_visible()
        assert self.footer.assert_footer_links_visible()

    def assert_products_visible(self, product_name: str) -> None:
        product_count = self.get_product_count()
        assert product_count > 0, "Expected products to be visible on the Home Page, but none found."