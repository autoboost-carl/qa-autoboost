from pages.base_page import BasePage

class LoginPage(BasePage):

    EMAIL_INPUT = "#loginFrm_loginname"
    PASSWORD_INPUT = "#loginFrm_password"
    LOGIN_BUTTON = "button[title='Login']"

    def login(self, username: str, password: str):
        self.page.fill(self.EMAIL_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)