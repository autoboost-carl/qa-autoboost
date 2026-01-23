from playwright.sync_api import Page, Locator, expect
from typing import Optional

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url, wait_until="networkidle")
    
    # ======================
    # Interaction Methods
    # ======================
    def click_element(self, locator: str | Locator) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.click()
    
    def fill_input(self, locator: str | Locator, text: str) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.fill(text)
    
    def type_text(self, locator: str | Locator, text: str, delay: int = 50) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.type(text, delay=delay)

    def select_option(self, locator: str | Locator, value: str) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.select_option(value)
    
    def check_box_radio(self, locator: str | Locator) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.check()
    
    def uncheck_box_radio(self, locator: str | Locator) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.uncheck()
    
    def hover_over_element(self, locator: str | Locator) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.hover()
    
    
    # ======================
    # Getting information
    # ======================
    def get_title(self) -> str:
        return self.page.title()
    
    def get_text(self, locator: str | Locator) -> str:
        if isinstance(locator, str):
            locator = self.page.locator(locator)
        text = locator.text_content()
        return text.strip() if text else ""
    
    def get_attribute(self, locator: str | Locator, attribute_name: str) -> Optional[str]:
        if isinstance(locator, str):
            locator = self.page.locator(locator)
        # We get HTML attributes
        return locator.get_attribute(attribute_name)

    # ======================
    # Wait Methods
    # ======================
    def wait_for_element(self, locator: str | Locator, timeout: int = 30000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.wait_for(state="visible", timeout=timeout)
    
    def wait_for_url(self, url_pattern: str, timeout: int = 30000) -> None:
        self.page.wait_for_url(f"**{url_pattern}**", timeout=timeout)

    def wait_for_load_state(self, state: str = "networkidle") -> None:
        self.page.wait_for_load_state(state=state)

    # ======================
    # Verification Methods
    # ======================
    def is_visible(self, locator: str | Locator) -> bool:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        return locator.is_visible()
    
    def is_enabled(self, locator: str | Locator) -> bool:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        return locator.is_enabled()
    
    def is_checked(self, locator: str | Locator) -> bool:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        return locator.is_checked()
    
    def count_elements(self, locator: str | Locator) -> int:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        return locator.count()
    
    # ======================
    # Assertion Methods         
    # ======================
    def assert_element_visible(self, locator: str | Locator) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible()
    
    def assert_text_equals(self, locator: str | Locator, expected_text: str) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_have_text(expected_text)
    
    def assert_text_contains(self, locator: str | Locator, expected_substring: s) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_contain_text(expected_substring)
    
    # ======================
    # Utility Methods
    # ======================
    def take_screenshot(self, filename: str, full_page: bool = False) -> None:
        self.page.screenshot(path=filename, full_page=full_page)
    
    def reload_page(self) -> None:
        self.page.reload()
    
    def scroll_to_element(self, locator: str | Locator) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        locator.scroll_into_view_if_needed()
    
