from logger import Logger
from selenium_core import SeleniumCore
from locators.registration_locators import HomePage, LoginPage


class AppFunctions(object):
    def __init__(self):
        self.logger = Logger.__call__().get_logger()
        self.core = SeleniumCore()

    def login(self, host, username, password):
        self.logger.info(f"Logging in to application, host: {host}, username: {username}, password: {password}")
        self.core.open_url(host)
        self.core.click(HomePage.sign_in_button)
        self.core.element_load_wait(LoginPage.authentication_header)
        self.core.input_text(LoginPage.email_textbox, username)
        self.core.input_text(LoginPage.password_textbox, password)
        self.core.click(LoginPage.login_button)
