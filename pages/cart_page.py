from playwright.sync_api import Page, Locator, expect
from pages.base.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.footer_component import FooterComponent
import re

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
    
        # Cart URL
        self.url = "https://automationteststore.com/index.php?rt=checkout/cart"

        # Reusable components
        self.header = HeaderComponent(page)
        self.footer = FooterComponent(page)

    #=====================================
    # Locators - Cart Structure
    #=====================================

    @property
    def cart_table(self):
        return self.page.locator("table.table-striped")
    
    @property
    def cart_items(self):
        return self.page.locator("table.table-striped tbody tr")
    
    @property
    def empty_cart_message(self):
        return self.page.locator("div.contentpanel").filter(has_text=re.compile(r"shopping cart is empty", re.IGNORECASE))
    
    #=====================================
    # Locators - Product elements on cart
    #=====================================

    def get_product_row_by_name(self, product_name: str):
        # Check for row containing product name
        return self.page.locator("table.table-striped tbody tr").filter(has_text=product_name)
    
    def qty_input_in_row(self, row: Locator) -> Locator:
        # Quantity input typically named "quantity[...]" or similar
        return row.locator("input[type='text'][name*='quantity']").first

    def remove_button_in_row(self, row: Locator) -> Locator:
        # Remove often via a trash icon 
        return row.locator("a[href*='remove'], a:has(i.fa-trash)").first

    @property
    def get_update_button(self):
        """This button updates the shopping cart after you change a qty"""
        return self.page.locator("button#cart-update")
    
    #=====================================
    # Locators - Checkout & Continue
    #=====================================

    @property
    def checkout_button(self):
        # Use the checkout link in the header menu with valid href
        # This one goes to checkout/shipping
        return self.page.locator("a.menu_checkout").first

    @property
    def continue_shopping_button(self):
        return self.page.locator("a:has-text('Continue Shopping')").first
    
    #=====================================
    # Actions - Navigation
    #=====================================

    def navigate_to_cart(self) -> None:
        self.navigate(self.url)
        # either empty message OR cart table visible
        if self.empty_cart_message.is_visible(timeout=1500):
            return
        expect(self.cart_table).to_be_visible(timeout=10_000)
    
    #=====================================
    # Actions - Cart Management
    #=====================================

    def update_qty(self, product_name: str, new_qty: int) -> None:
        # Getting the row for the product
        row = self.get_product_row_by_name(product_name)
        expect(row).to_be_visible(timeout=10_000)

        # Obtaining qty input
        qty_input = self.qty_input_in_row(row)
        expect(qty_input).to_be_visible(timeout=10_000)

        # Clear and write a new qty
        self.fill_input(qty_input, str(new_qty))

        # Try to click update button if it exists
        update_btn = self.get_update_button
        if update_btn.is_visible(timeout=1500):
            self.click_element(update_btn)
        else:
            qty_input.press("Enter") # If no update button, press Enter on the input field

        # Input value becomes new qty
        expect(qty_input).to_have_value(str(new_qty), timeout=10_000)
    
    def remove_product(self, product_name: str) -> None:
        # Getting the row for the product
        row = self.get_product_row_by_name(product_name)
        expect(row).to_be_visible(timeout=10_000)
        
        remove_button = self.remove_button_in_row(row)
        self.click_element(remove_button)

        # Row disappears
        expect(row).not_to_be_visible(timeout=10_000)
    
    def proceed_to_checkout(self) -> None:
        """Navigate to checkout by going to the shipping page"""
        # If the checkout button exists, prefer clicking it 
        if self.checkout_button.is_visible(timeout=1500):
            self.click_element(self.checkout_button)
        else:
            self.navigate("https://automationteststore.com/index.php?rt=checkout/shipping")
        
        # Assert you're on a checkout URL
        expect(self.page).to_have_url(re.compile(r"rt=checkout/"), timeout=10_000)
    
    def continue_shopping(self) -> None:
        self.click_element(self.continue_shopping_button)
        self.wait_for_load_state()
    
    #=====================================
    # Actions - Obtaining info
    #=====================================
    
    def get_cart_item_count(self) -> int:
        """Obtaining the count of unique items on the cart"""
        if self.is_cart_empty():
            return 0
        # Count product rows
        return self.count_elements(self.cart_items)
    
    def get_quantity_for_product(self, product_name: str) -> int:
        row = self.get_product_row_by_name(product_name)
        expect(row).to_be_visible(timeout=10_000)

        qty_input = self.qty_input_in_row(row)
        expect(qty_input).to_be_visible(timeout=10_000)

        qty_value = qty_input.input_value()
        return int(qty_value) if qty_value else 0
    
    #=====================================
    # Verifications
    #=====================================

    def is_cart_empty(self) -> bool:
        return self.empty_cart_message.is_visible()
    
    def is_product_in_cart(self, product_name: str) -> bool:
        product_row = self.get_product_row_by_name(product_name)
        return product_row.is_visible(timeout=1500)
        
    def is_checkout_button_visible(self) -> bool:
        return self.checkout_button.is_visible(timeout=1500)
    
    #=====================================
    # Assertions
    #=====================================

    def assert_cart_not_empty(self) -> None:
        assert not self.is_cart_empty(), "Cart is empty but should contain items"
    
    def assert_cart_empty(self) -> None:
        assert self.is_cart_empty(), "Cart contains items but should be empty"
    
    def assert_product_in_cart(self, product_name: str) -> None:
        row = self.get_product_row_by_name(product_name)
        expect(row).to_be_visible(timeout=10_000)
    
    def assert_product_not_in_cart(self, product_name: str) -> None:
        row = self.get_product_row_by_name(product_name)
        expect(row).not_to_be_visible(timeout=10_000)
    
    def assert_product_qty(self, product_name: str, expected_qty: int) -> None:
        row = self.get_product_row_by_name(product_name)
        expect(row).to_be_visible(timeout=10_000)

        qty_input = self.qty_input_in_row(row)
        expect(qty_input).to_have_value(str(expected_qty), timeout=10_000)
    
    
