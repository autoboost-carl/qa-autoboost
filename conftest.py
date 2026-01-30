import pytest
import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page, BrowserContext
import os
from datetime import datetime
from dotenv import load_dotenv
from test_data.test_data import TestDataGenerator

# Load environment variables from .env file
load_dotenv()

#=====================
# Page configuration
#=====================
@pytest.fixture
def page(context: BrowserContext) -> Page:
    # Create a new page for each test
    page = context.new_page()
    # Deliver the page to the test
    yield page
    # Close the page after the test
    page.close()

#=====================
# Base URL configuration
#=====================
@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://automationteststore.com/")

#=====================
# Automatic screenshot on failure
#=====================
@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    # Execute the test
    yield
    # If the test failed, take a screenshot
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # Create screenshot with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/{request.node.name}_{timestamp}.png"
        # Ensure the screenshots directory exists
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        # Take screenshot
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

#=====================
# Hook to capture test results
#=====================
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # Set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, f"rep_{rep.when}", rep)

#=====================
# Test Data Fixtures - E2E Tests
#=====================

@pytest.fixture
def guest_checkout_data():
    """Fixture for guest checkout test data"""
    return TestDataGenerator.generate_guest_checkout_data()

@pytest.fixture
def registered_user_data():
    """Fixture for registered user credentials"""
    return TestDataGenerator.generate_registered_user_data()

@pytest.fixture
def registered_user_checkout_data():
    """Fixture for registered user checkout data"""
    return TestDataGenerator.generate_registered_user_checkout_data()

@pytest.fixture
def multiple_products_data():
    """Fixture for multiple products cart test data"""
    return TestDataGenerator.generate_multiple_products_data()

#=====================
# Test Data Fixtures - Page Objects
#=====================

@pytest.fixture
def product_search_data():
    """Fixture for common product search queries"""
    return {
        "shirt": "shirt",
        "shoes": "shoes",
        "conditioner": "conditioner",
        "perfume": "perfume",
        "shampoo": "shampoo",
        "cream": "cream"
    }

@pytest.fixture
def invalid_login_data():
    """Fixture for invalid login credentials"""
    return {
        "email": "invalid@example.com",
        "password": "WrongPassword123!"
    }

@pytest.fixture
def valid_login_data():
    """Fixture for valid login credentials"""
    return {
        "email": os.getenv("VALID_EMAIL", "registereduser@example.com"),
        "password": os.getenv("VALID_PASSWORD", "TestPassword123!")
    }

@pytest.fixture
def generate_data_for_contact_us():
    """Fixture for contact us form data"""
    return TestDataGenerator.generate_data_for_contact_us()

#============================
# Allure Reports
#============================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            # Screenshot
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot",
                attachment_type=AttachmentType.PNG,
            )
            # Page HTML
            allure.attach(
                page.content(),
                name="page_source",
                attachment_type=AttachmentType.HTML,
            )