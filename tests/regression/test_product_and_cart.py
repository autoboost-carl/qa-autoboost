import pytest
import allure
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

@allure.feature("Search functionality")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_navigate_to_product_from_home(page: Page):
    home_page = HomePage(page)
    product_page = ProductPage(page)

    home_page.navigate_to_home()

    # Search for a product and press enter
    home_page.header.search_product_with_key("shirt")

    # Click on the first result
    first_product = page.locator("a.prdocutname, a.productname").first
    first_product.click()
    page.wait_for_load_state("domcontentloaded")

    # Check we're on a product page
    product_page.assert_on_product_page()

    print("Navigation to product page works")

@allure.feature("Shopping Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_add_product_to_cart(page: Page):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    home_page.navigate_to_home()

    # Search for a product
    home_page.header.search_product_with_button("shoes")

    # Click on the first product
    first_product = page.locator("a.prdocutname, a.productname").first
    first_product.click()
    page.wait_for_load_state("domcontentloaded")

    # Check we're on a product page
    product_page.assert_on_product_page()

    # Add to cart
    product_page.add_to_cart()
    page.wait_for_load_state("networkidle")

    # Assert we're on the cart
    cart_page.assert_cart_not_empty()
    print("Product was added successfully to the cart")

@allure.feature("Shopping Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_add_multiple_quantities_to_cart(page: Page):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    # Navigate and search product
    home_page.navigate_to_home()
    home_page.header.search_product_with_button("cream")

    # Click on the product
    first_product = page.locator("a.prdocutname, a.productname").first
    first_product.click()
    page.wait_for_load_state("domcontentloaded")

    # Add several units i.e. 3
    product_page.add_to_cart_with_quantity(3)
    page.wait_for_load_state("networkidle")

    # Assert cart's not empty
    cart_page.assert_cart_not_empty()

    print("Multiple quantities added to cart")

@allure.feature("Shopping Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_remove_product_from_cart(page: Page):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    # Navigate and search product
    home_page.navigate_to_home()
    home_page.header.search_product_with_button("shampoo")

    # Click on the product
    first_product = page.locator("a.prdocutname, a.productname").first
    first_product.click()
    page.wait_for_load_state("domcontentloaded")

    # Add to cart
    product_page.add_to_cart()
    page.wait_for_load_state("networkidle")

    # Add another product
    home_page.header.search_product_with_button("perfume")
    first_product = page.locator("a.prdocutname, a.productname").first
    first_product.click()
    page.wait_for_load_state("domcontentloaded")
    product_page.add_to_cart()
    page.wait_for_load_state("networkidle")

    # Remove the products
    cart_page.remove_product("shampoo")
    page.wait_for_load_state("domcontentloaded")
    cart_page.remove_product("perfume")
    page.wait_for_load_state("domcontentloaded")

    # Assert cart's empty
    cart_page.assert_cart_empty()

    print("Products were removed and cart's empty")


