from playwright.sync_api import Page
from pages.base.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.footer_component import FooterComponent

class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Reusable components
        self.header = HeaderComponent(page)
        self.footer = FooterComponent(page)

    #=====================================
    # Locators - Product Info
    #=====================================

    @property
    def product_name(self):
        return self.page.locator("h1.productname")
        
    @property
    def product_price(self):
        return self.page.locator("div.productprice")
        
    @property
    def product_description(self):
        return self.page.locator("div#description")
        
    @property
    def product_main_image(self):
        return self.page.locator("a.local_image")
        
    #=====================================
    # Locators - Options & Qty
    #=====================================

    @property
    def quantity_input(self):
        return self.page.locator("input#product_quantity")
        
    @property
    def add_to_cart_button(self):
        return self.page.locator("a.cart")
        
        
    #=====================================
    # Locators - Size, Color, etc.
    #=====================================

    @property
    def get_option_dropdown(self, option_name: str):
        """option_name: 'Size', 'Color'"""
        # Options are on id with option
        # i.e. (id="option350" is color, etc.)
        return self.page.locator(f"select[name=*'option']")
        
    #=====================================
    # Actions 
    #=====================================

    def set_quantity(self, quantity: int) -> None:
       self.quantity_input.fill(str(quantity)) 
        
    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()
        self.page.wait_for_timeout(1000)
        
    def add_to_cart_with_quantity(self, quantity: int) -> None:
        self.set_quantity(quantity)
        self.add_to_cart()
        
    def select_option(self, option_name: str, option_value: str) -> None:
        option_dropdown = self.get_option_dropdown(option_name)
        
        # Select by visible text (label)
        option_dropdown.select_option(label=option_value)
        
    #=====================================
    # Actions - Obtaining info
    #=====================================

    def get_product_name(self) -> str:
        return self.get_text(self.product_name)
        
    def get_product_price(self) -> str:
        price_text = self.get_text(self.product_price)
        return price_text.strip()
        
    def get_current_quantity(self) -> int:
        # Obtaining input value
        qty_value = self.quantity_input.input_value()
        # Converting to int
        return int(qty_value) if qty_value else 1

    #=====================================
    # Verifications
    #=====================================

    def is_on_product_page(self) -> bool:
        # Check product name is visible
        name_check = self.product_name.is_visible()
        # Verify Add to cart button is visible
        button_check = self.add_to_cart_button.is_visible()
       
        return name_check and button_check
        
    def is_add_to_cart_button_enabled(self) -> bool:
        return self.add_to_cart_button.is_enabled()
        
    
    #=====================================
    # Assertions
    #=====================================

    def assert_on_product_page(self) -> None:
        assert self.is_on_product_page(), "Not on product page"

        # Check key elements
        self.assert_element_visible(self.product_name)
        self.assert_element_visible(self.product_price)
        self.assert_element_visible(self.add_to_cart_button)
        
        