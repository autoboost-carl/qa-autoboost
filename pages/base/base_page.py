from playwright.sync_api import Page, Locator, expect
from typing import Optional, Pattern, Union

UrlPattern = Union[str, Pattern[str]]

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")
    
    # ======================
    # Interaction Methods
    # ======================
    def click_element(self, locator: str | Locator, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        expect(locator).to_be_enabled(timeout=timeout)
        locator.click(timeout=timeout)
    
    def fill_input(self, locator: str | Locator, text: str, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        locator.fill(text, timeout=timeout)
    
    def type_text(self, locator: str | Locator, text: str, delay: int = 50, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        locator.type(text, delay=delay, timeout=timeout)


    def select_option(self, locator: str | Locator, value: str, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        locator.select_option(value=value, timeout=timeout)
    
    def check_box_radio(self, locator: str | Locator, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        locator.check(timeout=timeout)
    
    def uncheck_box_radio(self, locator: str | Locator, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        locator.uncheck(timeout=timeout)
    
    def hover_over_element(self, locator: str | Locator, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        locator.hover(timeout=timeout)
    
    
    # ======================
    # Getting information
    # ======================
    def get_title(self) -> str:
        return self.page.title()
    
    def get_text(self, locator: str | Locator, timeout: int = 10000) -> str:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        text = locator.inner_text(timeout=timeout)
        return text.strip() if text else ""
    
    def get_attribute(self, locator: str | Locator, attribute_name: str, timeout: int = 10000) -> Optional[str]:
        if isinstance(locator, str):
            locator = self.page.locator(locator)
        
        expect(locator).to_be_attached(timeout=timeout)
        return locator.get_attribute(attribute_name)

    # ======================
    # Wait Methods
    # ======================
    def wait_for_element(self, locator: str | Locator, timeout: int = 30000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
    
    def wait_for_url(self, url_pattern: UrlPattern, timeout: int = 30000) -> None:
        if isinstance(url_pattern):
            self.page.wait_for_url(f"**{url_pattern}**", timeout=timeout)
        else:
            expect(self.page).to_have_url(url_pattern, timeout=timeout)

    def wait_for_load_state(self, state: str = "domcontentloaded") -> None:
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
    def assert_element_visible(self, locator: str | Locator, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
    
    def assert_text_equals(self, locator: str | Locator, expected_text: str, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_have_text(expected_text, timeout=timeout)
    
    def assert_text_contains(self, locator: str | Locator, expected_substring: str, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_contain_text(expected_substring, timeout=timeout)
    
    # ======================
    # Utility Methods
    # ======================
    def take_screenshot(self, filename: str, full_page: bool = False) -> None:
        self.page.screenshot(path=filename, full_page=full_page)
    
    def reload_page(self) -> None:
        self.page.reload()
    
    def scroll_to_element(self, locator: str | Locator, timeout: int = 10000) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        expect(locator).to_be_visible(timeout=timeout)
        locator.scroll_into_view_if_needed()
    
