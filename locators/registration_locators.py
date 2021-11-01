
class HomePage(object):
    sign_in_button = '//a[@class="login"]'


class LoginPage(object):
    authentication_header = '//h1[text()="Authentication"]'
    email_textbox = '//input[@id="email"]'
    password_textbox = '//input[@id="passwd"]'
    login_button = '//button[@id="SubmitLogin"]'
    account_creation_form = '//form[@id="create-account_form"]'
    create_email_textbox = '//input[@id="email_create"]'
    create_account_button = '//button[@id="SubmitCreate"]'


class RegistrationPage(object):
    # below are 'Your personal information' section locators
    registration_header = '//h1[text()="Create an account"]'
    gender_mr_checkbox = '//input[@id="id_gender1"]'
    gender_mrs_checkbox = '//input[@id="id_gender2"]'
    first_name_textbox = '//input[@id="customer_firstname"]'
    last_name_textbox = '//input[@id="customer_lastname"]'
    password_textbox = '//input[@id="passwd"]'
    days_dropdown = '//select[@id="days"]/option[@value="%s"]'
    months_dropdown = '//select[@id="months"]/option[@value="%s"]'
    years_dropdown = '//select[@id="years"]/option[@value="%s"]'

    # below are 'Your address' section locators
    address_first_name_textbox = '//input[@id="firstname"]'
    address_last_name_textbox = '//input[@id="lastname"]'
    company_textbox = '//input[@id="company"]'
    address_textbox = '//input[@id="address1"]'
    address2_textbox = '//input[@id="address2"]'
    city_textbox = '//input[@id="city"]'
    state_dropdown = '//select[@id="id_state"]/option[text()="%s"]'
    postcode_textbox = '//input[@id="postcode"]'
    add_info_textbox = '//input[@id="other"]'
    home_phone_textbox = '//input[@id="phone"]'
    mobile_textbox = '//input[@id="phone_mobile"]'
    register_button = '//button[@id="submitAccount"]'


class AccountPage(object):
    account_header = '//h1[text()="My account"]'
