import os
import pytest
import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page, BrowserContext
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
# Hook: report + Allure attachments + rep_call attribute
#=====================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Keep these attributes so other fixtures can check failures
    setattr(item, f"rep_{rep.when}", rep)

    # Attach to Allure only on test failure
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot",
                attachment_type=AttachmentType.PNG,
            )
            allure.attach(
                page.content(),
                name="page_source",
                attachment_type=AttachmentType.HTML,
            )

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

