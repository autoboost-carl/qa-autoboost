import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
@pytest.mark.p0
def test_home_page_loads(page: Page, base_url: str):
    # Navigate to the home page
    page.goto(base_url)
    # Verify that the home page title is correct
    expect(page).to_have_title("A place to practice your automation skills!")
    # Verify logo is visible
    logo = page.locator("img[alt='Automation Test Store']")
    expect(logo).to_be_visible()

    print("Home page loaded successfully")

@pytest.mark.smoke
@pytest.mark.p0
def test_main_navigation_visible(page: Page, base_url: str):
    # Navigate to the home page
    page.goto(base_url)

    main_menu = page.locator("nav.subnav")
    expect(main_menu).to_be_visible()

    # Verify count of navigation links
    nav_links = main_menu.locator("ul.nav-pills > li > a")
    expect(nav_links).to_have_count(8)
    print("Categories nav bar is visible on the home page with correct number of links")

    # Print out the navigation link texts
    all_links = nav_links.all()

    print("\n Navigation links found:")
    for i, link in enumerate(all_links):
        text = link.text_content()
        print(f" {i + 1}. [{text.strip()}]")

#@pytest.mark.smoke
#def test_screenshot_on_failure(page: Page, base_url: str):
#    # Navigate to the home page
#    page.goto(base_url)
#    # Intentionally fail the test to trigger screenshot capture
#    expect(page).to_have_title("This title is incorrect to trigger failure")
   
    