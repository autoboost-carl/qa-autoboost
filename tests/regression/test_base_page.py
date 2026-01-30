import pytest
from playwright.sync_api import Page
from pages.base.base_page import BasePage

@pytest.mark.regression
def test_base_page_methods(page: Page, base_url: str):
    # Instantiate BasePage
    base_page = BasePage(page)  

    # Navigate to home page
    base_page.navigate(base_url)
   
    # Click on a button
    button_locator = page.get_by_role("link", name="Books")
    base_page.click_element(button_locator)
   

    # Hover over an element
    hover_locator = page.get_by_role("link", name="Hair Care")
    base_page.hover_over_element(hover_locator)
    base_page.page.wait_for_timeout(3000)  # Wait for 3 seconds
   
    # fill an input field
    search_input_locator = page.locator("input[name='filter_keyword']")
    base_page.click_element(search_input_locator)
    base_page.fill_input(search_input_locator, "Shoes")
    base_page.click_element(page.locator(".fa.fa-search"))  
    base_page.page.wait_for_timeout(3000)  # Wait for 3 seconds