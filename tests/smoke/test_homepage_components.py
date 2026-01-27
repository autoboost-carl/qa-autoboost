import pytest 
from playwright.sync_api import Page
from pages.home_page import HomePage

@pytest.mark.smoke
def test_homepage_components(page: Page, base_url: str):
    """Verify the presence and functionality of key homepage components."""
    home_page = HomePage(page)
    home_page.navigate_to_home()

    # Verify that we are on the home page with header and footer components visible
    home_page.assert_on_home_page()

    print("Header and Footer components are present and functional on the Home Page.")

@pytest.mark.smoke
def test_logo_navigation_to_home(page: Page, base_url: str):
    """Verify that clicking the logo navigates to the home page."""
    home_page = HomePage(page)
    home_page.navigate_to_home()

    # Click on the logo in the header
    home_page.header.click_logo()

    # Verify navigation to home page
    home_page.assert_on_home_page()

    print("Clicking the logo successfully navigates to the Home Page.")

@pytest.mark.smoke
def test_search_existing_product(page: Page, base_url: str):
    home_page = HomePage(page)
    home_page.navigate_to_home()

    sample_product = "shirt"
    home_page.header.search_product_with_key(sample_product)

    # This will raise AssertionError if anything fails
    home_page.header.assert_search_results(sample_product)

    print(f"Search functionality works correctly for the term '{sample_product}'.")

    