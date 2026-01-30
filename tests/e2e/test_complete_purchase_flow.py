"""
E2E tests for complete purchase flow
These tests verify the full checkout process for different user types
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from utils.helpers import ProductHelpers
from dotenv import load_dotenv
import os


@allure.epic("E2E Purchase Flow")
@allure.feature("Guest Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_complete_purchase_flow_as_guest(page: Page, guest_checkout_data):
    """
    E2E test for complete purchase flow as guest
    
    Steps:
    1. Navigate to home
    2. Search for product
    3. Add product to cart
    4. View cart
    5. Proceed to checkout as guest
    6. Fill checkout information
    7. Confirm order
    8. Verify order successful
    """
    # Initialize page objects
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    
    with allure.step("Navigate to home page"):
        # Step 1: Navigate to home
        home_page.navigate_to_home()
        home_page.assert_on_home_page()
    
    with allure.step("Search for product"):
        # Step 2: Search for product
        home_page.header.search_product_with_button(guest_checkout_data["product_search"])
        page.wait_for_load_state("networkidle")
    
    with allure.step("Select first product from results and add it to the cart"):
        # Step 3: Add product to cart
        first_product = page.locator("a.prdocutname, a.productname").first
        assert first_product.count() > 0, f"❌ Product '{guest_checkout_data['product_search']}' not found in search results"
        first_product.click()
        page.wait_for_load_state("domcontentloaded")
        product_page.assert_on_product_page()
        product_page.add_to_cart()
        print(f"{guest_checkout_data["product_search"]} was added successfully")
        page.wait_for_load_state("networkidle")
    
    with allure.step("Verify the product was added successfully and the cart is not empty"):
        # Step 4: Assert cart product
        cart_page.assert_cart_not_empty()
        cart_page.assert_product_in_cart(guest_checkout_data["product_search"])
        print(f"{guest_checkout_data["product_search"]} is included in the cart")

    with allure.step("Proceed to checkout"):
        # Step 5: Proceed to checkout as guest
        cart_page.proceed_to_checkout()
        checkout_page.assert_on_checkout_page()
    
    with allure.step("Fill checkout information"):
        # Step 6: Fill checkout information
        checkout_page.select_guest_checkout()
        page.wait_for_load_state("networkidle")
    
        checkout_page.fill_guest_information(
            email=guest_checkout_data["email"],
            firstname=guest_checkout_data["firstname"],
            lastname=guest_checkout_data["lastname"],
            address=guest_checkout_data["address"],
            city=guest_checkout_data["city"],
            zipcode=guest_checkout_data["zipcode"],
            phone=guest_checkout_data["phone"],
            country=guest_checkout_data.get("country", "United States"),
            state=guest_checkout_data.get("state", "New York")
        )

    print("Guest form was filled successfully")
    
    with allure.step("Click on confirm order"):
        # Step 7: Confirm order
        checkout_page.confirm_order()
    
    with allure.step("Verify your order has been processed"):
        # Step 8: Verify order successful
        checkout_page.wait_for_order_confirmation()
        checkout_page.assert_order_confirmed()
        
    print("Purchase Order is confirmed")
    print("✅ Guest checkout E2E test passed")

@allure.epic("E2E Purchase Flow")
@allure.feature("Registered User Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_complete_purchase_flow_as_registered_user(page: Page, registered_user_checkout_data):
    """
    E2E test for complete purchase flow as registered user
    
    Steps:
    1. Navigate to home
    2. Search for product
    3. Add product to cart
    4. View cart
    5. Proceed to checkout and login
    6. Fill shipping information
    7. Confirm order
    8. Verify order successful
    """
    # Initialize page objects
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    login_page = LoginPage(page)

    # Load environment variables from .env file
    load_dotenv()
    
    with allure.step("Navigate to home page"):
        # Step 1: Navigate to home
        home_page.navigate_to_home()
        home_page.assert_on_home_page()
    
    with allure.step("Search for product"):
        # Step 2: Search for product
        home_page.header.search_product_with_button(registered_user_checkout_data["product_search"])
        page.wait_for_load_state("networkidle")
    
    with allure.step("Select first product from results and add it to the cart"):
        # Step 3: Add product to cart
        first_product = page.locator("a.prdocutname, a.productname").first
        assert first_product.count() > 0, f"❌ Product '{registered_user_checkout_data['product_search']}' not found in search results"
        first_product.click()
        page.wait_for_load_state("domcontentloaded")
        product_page.assert_on_product_page()
        product_page.add_to_cart()
        print(f"{registered_user_checkout_data["product_search"]} was added successfully")
        page.wait_for_load_state("networkidle")
    
    with allure.step("Verify the product got added and the cart is not empty"):
        # Step 4: Assert cart product
        cart_page.assert_cart_not_empty()
        cart_page.assert_product_in_cart(registered_user_checkout_data["product_search"])
        print(f"{registered_user_checkout_data["product_search"]} is included in the cart")

    with allure.step("Proceed to checkout and login with an existing user"):
        # Step 5: Proceed to checkout and login
        cart_page.proceed_to_checkout()
        checkout_page.assert_on_checkout_page()

        valid_login_name = os.getenv("VALID_LOGIN_NAME")
        valid_password = os.getenv("VALID_PASSWORD")
    
        login_page.login(valid_login_name, valid_password)
        page.wait_for_load_state("networkidle")

    print("Login with registered user was successful")
    
    with allure.step("Click on confirm order"):
        # Step 6: Confirm order
        checkout_page.confirm_order()
    
    with allure.step("Verify your order has been processed"):
        # Step 7: Verify order successful
        checkout_page.wait_for_order_confirmation()
        checkout_page.assert_order_confirmed()

    print("Purchase Order is confirmed")
    print("✅ Registered user checkout E2E test passed")


@allure.epic("E2E Purchase Flow")
@allure.feature("Cart management with more than one product")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_cart_management_multiple_products_flow(page: Page, multiple_products_data):
    """
    E2E test for cart management with multiple products
    
    Steps:
    1. Add product 1 to cart (with alternatives if not found)
    2. Continue shopping
    3. Add product 2 to cart (with alternatives if not found)
    4. View cart with both products
    5. Update quantity of product 1
    6. Remove product 2
    7. Proceed to checkout with product 1
    8. Complete purchase as guest
    """
    # Initialize page objects
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    
    with allure.step("Navigate to home page and add a product"):
        # Step 1: Navigate to home and add product 1
        home_page.navigate_to_home()
        page.wait_for_load_state("networkidle")
    
        product_1_name, product_1_found = ProductHelpers.search_and_add_product(
            home_page, product_page, page,
            multiple_products_data["product_1_search"],
            multiple_products_data.get("product_1_alternatives", [])
        )
    
        assert product_1_found, "❌ Could not find product 1 or any alternatives"
    
    with allure.step("Continue shopping"):
        # Step 2: Continue shopping
        home_page.navigate_to_home()
        page.wait_for_load_state("networkidle")
    
    with allure.step("Add another product"):
        # Step 3: Add product 2 to cart
        product_2_name, product_2_found = ProductHelpers.search_and_add_product(
            home_page, product_page, page,
            multiple_products_data["product_2_search"],
            multiple_products_data.get("product_2_alternatives", [])
        )
    
        if not product_2_found:
            print("⚠️  Product 2 not found, continuing with only product 1")
    
    with allure.step("View your cart to ensure is not empty"):
        # Step 4: View cart
        cart_page.navigate_to_cart()
        cart_page.assert_cart_not_empty()
    
        # Verify product 1 is in cart
        assert cart_page.is_product_in_cart(product_1_name), f"Product 1 '{product_1_name}' not in cart"
        print(f"✓ Product 1 '{product_1_name}' verified in cart")
    
        # Verify product 2 is in cart if it was found
        if product_2_found:
            assert cart_page.is_product_in_cart(product_2_name), f"Product 2 '{product_2_name}' not in cart"
            print(f"✓ Product 2 '{product_2_name}' verified in cart")
    
    with allure.step("Update the quantity of the first product you added"):
        # Step 5: Update quantity of product 1
        initial_qty = cart_page.get_quantity_for_product(product_1_name)
        new_qty = initial_qty + 1
        cart_page.update_qty(product_1_name, new_qty)
        updated_qty = cart_page.get_quantity_for_product(product_1_name)
        assert updated_qty == new_qty, f"Quantity not updated. Expected {new_qty}, got {updated_qty}"
        print(f"✓ Product 1 quantity updated to {new_qty}")
    
    with allure.step("Remove the second product you added"):
        # Step 6: Remove product 2 if it was found
        if product_2_found:
            cart_page.remove_product(product_2_name)
            page.wait_for_load_state("networkidle")
            assert not cart_page.is_product_in_cart(product_2_name), \
                "Product 2 should be removed from cart"
            print(f"✓ Product 2 '{product_2_name}' removed from cart")
    
    with allure.step("Proceed to checkout"):
        # Step 7: Proceed to checkout with product 1
        cart_page.proceed_to_checkout()
        checkout_page.assert_on_checkout_page()
    
    with allure.step("Complete purchase as guest"):
        # Step 8: Complete purchase as guest
        checkout_page.select_guest_checkout()
        page.wait_for_load_state("networkidle")
    
        checkout_page.fill_guest_information(
            email=multiple_products_data["email"],
            firstname=multiple_products_data["firstname"],
            lastname=multiple_products_data["lastname"],
            address=multiple_products_data["address"],
            city=multiple_products_data["city"],
            zipcode=multiple_products_data["zipcode"],
            phone=multiple_products_data["phone"]
        )
    with allure.step("Confirm and verify your order has been processed"):
        # Step 9: Confirm and assert order
        checkout_page.confirm_order()
        checkout_page.wait_for_order_confirmation()
        checkout_page.assert_order_confirmed()
    
    print("✅ Cart management multiple products E2E test passed")
