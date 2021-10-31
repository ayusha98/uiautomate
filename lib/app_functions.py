import os
from logger import Logger
from config_parser import ParseXLS
from selenium_core import SeleniumCore
from locators.registration_locators import HomePage, LoginPage, RegistrationPage


class AppFunctions(object):
    def __init__(self):
        self.logger = Logger.__call__().get_logger()
        self.core = SeleniumCore()
        current_path = os.getcwd()
        self.conf_dir = os.path.join(current_path[:current_path.find('uiautomate')], 'uiautomate', 'conf')

    def launch_app(self, home_url):
        self.logger.info(f"Opening application home page, URL: {home_url}")
        try:
            assert self.core.open_url(home_url), f"Unable to launch the application URL: {home_url}"
            self.core.element_displayed(HomePage.sign_in_button)
            return True
        except AssertionError as e:
            self.logger.error(f"Failed to launch app, {e}")
        return False

    def login(self, username, password):
        self.logger.info(f"Logging in to application, username: {username}, password: {password}")
        try:
            assert self.core.click(HomePage.sign_in_button), "Unable to click on Sign In button on home page"
            assert self.core.element_load_wait(LoginPage.authentication_header), "Failed to verify the login page load"
            assert self.core.input_text(LoginPage.email_textbox, username), "Unable to enter username text on login page"
            assert self.core.input_text(LoginPage.password_textbox, password), "Unable to enter password text"
            assert self.core.click(LoginPage.login_button), "Unable to click on Login button"
            return True
        except AssertionError as e:
            self.logger.error(f"Something unexpected happened, {e}")
        return False

    def registration(self, filename, sheet_name, tag):
        sheet_list = ParseXLS(self.conf_dir, filename).main(sheet_name)
        row_list = [row for row in sheet_list if row['tag'] == str(tag)]
        if row_list:
            row_dict = row_list[0]
        else:
            self.logger.error(f"Specified tag seems to be invalid, there is no matching row for tag: {tag}")
            return False

        self.logger.info(f"Starting new user registration flow, user details: {row_dict}")
        try:
            assert self.core.click(HomePage.sign_in_button), "Unable to click on Home page Sign in button"
            assert self.core.element_load_wait(LoginPage.authentication_header), "Failed to verify the login page load"
            assert self.core.input_text(LoginPage.create_email_textbox, row_dict["email"]), "Unable to enter email text"
            assert self.core.click(LoginPage.create_account_button), "Unable to click on Create account button"
            assert self.core.element_load_wait(RegistrationPage.registration_header), \
                "Failed to verify the Registration page load"

            # now the registration page should be loaded, let's populate all the fields
            name = row_dict["name"]
            gender, first_name, last_name = name.split()[0], name.split()[1], name.split()[2]
            if gender.lower() == 'mr':
                assert self.core.click(RegistrationPage.gender_mr_checkbox), "Unable to click gender checkbox"
            else:
                assert self.core.click(RegistrationPage.gender_mrs_checkbox), "Unable to click on gender checkbox"
            assert self.core.input_text(RegistrationPage.first_name_textbox, first_name), "Unable to enter first name"
            assert self.core.input_text(RegistrationPage.last_name_textbox, last_name), "Unable to enter last name"
            assert self.core.input_text(RegistrationPage.password_textbox, row_dict["password"]), \
                "Unable to enter password field"
            day, month, year = row_dict["dob"].split('/')[0], row_dict["dob"].split('/')[1], row_dict["dob"].split('/')[2]
            assert self.core.click(RegistrationPage.days_dropdown % day), f"Unable to select Data of Birth, Day: {day}"
            assert self.core.click(RegistrationPage.months_dropdown % month), \
                f"Unable to select Data of Birth, Month: {month}"
            assert self.core.click(RegistrationPage.years_dropdown % year), \
                f"Unable to select Data of Birth, Year: {year}"

            # since Company is an optional field, let's first check if it is specified in the row detail
            if row_dict["company"]:
                assert self.core.input_text(RegistrationPage.company_textbox, row_dict["company"]), \
                    "Unable to enter Company name in address section"
            assert self.core.input_text(RegistrationPage.address_textbox, row_dict["address"]), \
                "Unable to enter address field"
            assert self.core.input_text(RegistrationPage.city_textbox, row_dict["city"]), "Unable to enter city field"
            assert self.core.click(RegistrationPage.state_dropdown % row_dict["state"]), \
                f"Unable to click on state: {row_dict['state']}"
            assert self.core.input_text(RegistrationPage.postcode_textbox, row_dict["zip_code"]), \
                "Unable to enter the zip code in address section"

            # optional fields check
            if row_dict["additional_info"]:
                assert self.core.input_text(RegistrationPage.add_info_textbox, row_dict["additional_info"]), \
                    "Unable to enter additional information in address section"
            if row_dict["home_phone"]:
                assert self.core.input_text(RegistrationPage.home_phone_textbox, row_dict["home_phone"]), \
                    "Unable to enter home phone in address section"
            assert self.core.input_text(RegistrationPage.mobile_textbox, row_dict["mobile"]), \
                "Unable to enter mobile phone no in address section"
            self.core.click(RegistrationPage.register_button)

            self.logger.info(f"Successfully completed new user registration flow, details: {row_dict}")
            return True
        except AssertionError as e:
            self.logger.error(f"Something unexpected happened, {e}")
        return False

    def quit(self):
        self.core.quit_browser()
