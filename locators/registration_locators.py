
class HomePage(object):
    sign_in_button = '//a[@class="login"]'


class LoginPage(object):
    authentication_header = '//h1[text()="Authentication"]'
    email_textbox = '//input[@id="email"]'
    password_textbox = '//input[@id="passwd"]'
    login_button = '//button[@id="SubmitLogin"]'
