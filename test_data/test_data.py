"""
Utility module for test data and helper functions
"""

class TestDataGenerator:
    """Generate test data for various test scenarios"""
    
    @staticmethod
    def generate_guest_checkout_data():
        """Generate guest checkout data"""
        return {
            "email": "testguest@example.com",
            "firstname": "John",
            "lastname": "Doe",
            "address": "123 Main Street",
            "city": "New York",
            "zipcode": "10001",
            "phone": "555-1234",
            "product_search": "shirt",
            "country": "United States",
            "state": "New York"
        }
    
    @staticmethod
    def generate_registered_user_data():
        """Generate registered user credentials"""
        return {
            "email": "registereduser@example.com",
            "password": "TestPassword123!",
            "username": "registereduser"
        }
    
    @staticmethod
    def generate_registered_user_checkout_data():
        """Generate checkout data for registered user"""
        return {
            "product_search": "conditioner",
            "email": "registereduser@example.com"
        }
    
    @staticmethod
    def generate_multiple_products_data():
        """Generate data for multiple products cart test"""
        return {
            "product_1_search": "hands",
            "product_1_alternatives": ["conditioner", "shampoo", "cream"],
            "product_2_search": "perfume",
            "product_2_alternatives": ["makeup", "shoes", "apparel"],
            "email": "testmultiproduct@example.com",
            "firstname": "Jane",
            "lastname": "Smith",
            "address": "456 Oak Avenue",
            "city": "Los Angeles",
            "zipcode": "90001",
            "phone": "555-5678"
        }
    @staticmethod
    def generate_data_for_contact_us():
        """Generate data for inquiry"""
        return {
            "firstname": "John",
            "email": "testguest@example.com",
            "enquiry": "I'm interested in buying hair conditioner on bulk. Would you give me a sweet discount? Thanks"
        }


class CartDataValidator:
    """Validate cart-related data and operations"""
    
    @staticmethod
    def validate_cart_item_count(current_count: int, expected_count: int) -> bool:
        """Validate if cart item count matches expected"""
        return current_count == expected_count
    
    @staticmethod
    def validate_product_quantity(current_qty: int, expected_qty: int) -> bool:
        """Validate if product quantity matches expected"""
        return current_qty == expected_qty


class OrderDataValidator:
    """Validate order-related data"""
    
    @staticmethod
    def validate_order_number_format(order_number: str) -> bool:
        """Validate if order number has valid format"""
        return bool(order_number) and len(order_number) > 0
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """Validate if email has correct format"""
        return "@" in email and "." in email.split("@")[1]
