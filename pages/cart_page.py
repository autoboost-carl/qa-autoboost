from playwright.sync_api import Page, Locator
from pages.base.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.footer_component import FooterComponent

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
        return self.page.locator("div.contentpanel:has-text('shopping cart is empty')")
    
    #=====================================
    # Locators - Product elements on cart
    #=====================================

    def get_product_row_by_name(self, product_name: str):
        # Check for row containing product name
        return self.page.locator(f"table.table-striped tbody tr:has-text('{product_name}')")
    
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
        self.wait_for_load_state("networkidle")
    
    #=====================================
    # Actions - Cart Management
    #=====================================

    def update_qty(self, product_name: str, new_qty: int) -> None:
        # Getting the row for the product
        row = self.get_product_row_by_name(product_name)
        
        # Obtaining qty input
        qty_input = self.qty_input_in_row(row)

        # Clear and write a new qty
        qty_input.fill(str(new_qty))

        # Try to click update button if it exists
        try:
            update_btn = self.get_update_button
            if update_btn.is_visible(timeout=3000):
                update_btn.click()
            else:
                # If no update button, press Enter on the input field
                qty_input.press("Enter")
        except:
            # If button doesn't exist or timeout, press Enter on the input field
            qty_input.press("Enter")
        
        # Wait for update
        self.wait_for_load_state("networkidle")
    
    def remove_product(self, product_name: str) -> None:
        # Getting the row for the product
        row = self.get_product_row_by_name(product_name)
        
        remove_button = self.remove_button_in_row(row)
        remove_button.click()

        self.wait_for_load_state("networkidle")
    
    def proceed_to_checkout(self) -> None:
        """Navigate to checkout by going to the shipping page"""
        # Navigate directly to shipping/checkout
        self.navigate("https://automationteststore.com/index.php?rt=checkout/shipping")
        self.wait_for_load_state("networkidle")
    
    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
        self.wait_for_load_state("networkidle")
    
    #=====================================
    # Actions - Obtaining info
    #=====================================
    
    def get_cart_item_count(self) -> int:
        """Obtaining the count of unique items on the cart"""
        if self.is_cart_empty():
            return 0
        # Count product rows
        return self.cart_items.count()
    
    def get_quantity_for_product(self, product_name: str) -> int:
        row = self.get_product_row_by_name(product_name)
        qty_input = self.qty_input_in_row(row)
        qty_value = qty_input.input_value()
        return int(qty_value) if qty_value else 0
    
    #=====================================
    # Verifications
    #=====================================

    def is_cart_empty(self) -> bool:
        return self.empty_cart_message.is_visible()
    
    def is_product_in_cart(self, product_name: str) -> bool:
        try:
            product_row = self.get_product_row_by_name(product_name)
            return product_row.is_visible()
        except:
            return False
        
    def is_checkout_button_visible(self) -> bool:
        """Check if checkout button is visible on the page"""
        try:
            return self.checkout_button.is_visible(timeout=5000)
        except:
            return False
    
    #=====================================
    # Assertions
    #=====================================

    def assert_cart_not_empty(self) -> None:
        assert not self.is_cart_empty(), "Cart is empty but should contain items"
    
    def assert_cart_empty(self) -> None:
        assert self.is_cart_empty(), "Cart contains items but should be empty"
    
    def assert_product_in_cart(self, product_name: str) -> None:
        assert self.is_product_in_cart(product_name), f"Product {product_name} not found in cart"
    
    def assert_product_not_in_cart(self, product_name: str) -> None:
        assert not self.is_product_in_cart(product_name), f"Product {product_name} found in cart but should not be there"
    
    def assert_product_qty(self, product_name: str, expected_qty: int) -> None:
        actual_qty = self.get_quantity_for_product(product_name)
        assert actual_qty == expected_qty, f"Expected quantity {expected_qty} for {product_name} but got {actual_qty} instead"
    
    
