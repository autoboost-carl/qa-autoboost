import pytest
import allure 
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.components.footer_component import FooterComponent

@pytest.mark.regression
def test_homepage_components(page: Page):
    """Verify the presence and functionality of key homepage components."""
    home_page = HomePage(page)
    home_page.navigate_to_home()

    # Verify that we are on the home page with header and footer components visible
    home_page.assert_on_home_page()

    print("Header and Footer components are present and functional on the Home Page.")

@pytest.mark.regression
def test_logo_navigation_to_home(page: Page):
    """Verify that clicking the logo navigates to the home page."""
    home_page = HomePage(page)
    home_page.navigate_to_home()

    # Click on the logo in the header
    home_page.header.click_logo()

    # Verify navigation to home page
    home_page.assert_on_home_page()

    print("Clicking on the logo successfully navigates to the Home Page.")
    
@allure.feature("Search functionality")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_search_existing_product(page: Page):
    home_page = HomePage(page)
    home_page.navigate_to_home()

    sample_product = "shirt"
    home_page.header.search_product_with_key(sample_product)

    # This will raise AssertionError if anything fails
    home_page.header.assert_search_results(sample_product)

    print(f"Search functionality works correctly for the term '{sample_product}'.")

@allure.feature("Contact Us")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_contact_us(page: Page, generate_data_for_contact_us):
    """Verify that the contact us page loads correctly"""
    home_page = HomePage(page)
    footer = FooterComponent(page)

    # Navigate to home
    home_page.navigate_to_home()

    # Click on contact us and verify navigation
    footer.click_contact_us()
    page.wait_for_load_state("networkidle")
    
    # Fill form and submit
    footer.fill_and_submit_contact_form(
        firstname=generate_data_for_contact_us["firstname"],
        email=generate_data_for_contact_us["email"],
        enquiry=generate_data_for_contact_us["enquiry"],
    )
    footer.assert_successful_contact_us()
    print("Inquiry was sent successfully")