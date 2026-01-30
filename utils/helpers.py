"""
Helper functions for test automation
"""

from datetime import datetime
import re


class WaitHelpers:
    """Helper functions for waiting and synchronization"""
    
    @staticmethod
    def generate_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
        """Generate a timestamp string"""
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def generate_unique_email(base_email: str = "test") -> str:
        """Generate unique email with timestamp"""
        timestamp = WaitHelpers.generate_timestamp("%Y%m%d%H%M%S")
        return f"{base_email}_{timestamp}@example.com"


class StringHelpers:
    """Helper functions for string manipulation"""
    
    @staticmethod
    def extract_number(text: str) -> str:
        """Extract first number sequence from text"""
        match = re.search(r'\d+', text)
        return match.group(0) if match else ""
    
    @staticmethod
    def extract_order_number(text: str) -> str:
        """Extract order number from text"""
        # Look for patterns like Order #12345
        match = re.search(r'Order\s*#?\s*(\d+)', text, re.IGNORECASE)
        return match.group(1) if match else ""
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text"""
        return " ".join(text.split())


class AssertionHelpers:
    """Custom assertion helpers for common checks"""
    
    @staticmethod
    def assert_contains(actual: str, expected: str, message: str = "") -> None:
        """Assert that actual string contains expected substring"""
        assert expected in actual, message or f"'{expected}' not found in '{actual}'"
    
    @staticmethod
    def assert_not_empty(value, message: str = "") -> None:
        """Assert that value is not empty"""
        assert value, message or "Value should not be empty"
    
    @staticmethod
    def assert_equals_ignorecase(actual: str, expected: str, message: str = "") -> None:
        """Assert that strings are equal ignoring case"""
        assert actual.lower() == expected.lower(), \
            message or f"'{actual}' != '{expected}' (case-insensitive)"


class URLHelpers:
    """Helper functions for URL operations"""
    
    @staticmethod
    def get_base_url() -> str:
        """Get base URL for the application"""
        return "https://automationteststore.com/"
    
    @staticmethod
    def get_full_url(path: str) -> str:
        """Get full URL with path"""
        base = URLHelpers.get_base_url()
        return f"{base}{path.lstrip('/')}"
    
    @staticmethod
    def extract_path_from_url(url: str) -> str:
        """Extract path from full URL"""
        # Remove protocol and domain
        if "://" in url:
            return "/" + url.split("://", 1)[1].split("/", 1)[1] if "/" in url.split("://", 1)[1] else "/"
        return url


class ProductHelpers:
    """Helper functions for product operations in tests"""
    
    @staticmethod
    def search_and_add_product(home_page, product_page, page, search_term, alternatives=None):
        """
        Search for a product and add to cart.
        If product not found, tries alternatives.
        
        Args:
            home_page: HomePage object
            product_page: ProductPage object
            page: Page object from Playwright
            search_term: Product name to search for
            alternatives: List of alternative products to try if first not found
            
        Returns:
            (product_name_added, success): Tuple with product name and success status
        """
        search_terms = [search_term]
        if alternatives:
            search_terms.extend(alternatives)
        
        for term in search_terms:
            try:
                home_page.header.search_product_with_button(term)
                page.wait_for_timeout(2000)
                
                # Check if any product results found
                first_product = page.locator("a.prdocutname, a.productname").first
                if first_product.count() == 0:
                    print(f"⚠️  No products found for '{term}', trying next alternative...")
                    home_page.navigate_to_home()
                    page.wait_for_timeout(1000)
                    continue
                
                # Product found, click and add to cart
                first_product.click()
                page.wait_for_timeout(2000)
                product_page.assert_on_product_page()
                product_page.add_to_cart()
                page.wait_for_timeout(2000)
                print(f"✓ Successfully added product: {term}")
                return term, True
            except Exception as e:
                print(f"⚠️  Error with product '{term}': {str(e)}")
                home_page.navigate_to_home()
                page.wait_for_timeout(1000)
                continue
        
        return None, False

