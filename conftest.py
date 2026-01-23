import pytest
from playwright.sync_api import Page, BrowserContext
import os
from datetime import datetime
from dotenv import load_dotenv

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