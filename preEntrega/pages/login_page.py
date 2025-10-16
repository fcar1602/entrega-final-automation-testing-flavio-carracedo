from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'input[type="submit"]')

    def open_login_page(self):
        self.open("https://www.saucedemo.com")

    def login(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)


