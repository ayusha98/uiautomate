from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from lib.app_functions import AppFunctions


class TC001(object):
    tc_id = "tc_id_001"
    tc_summary = "Verify that user is able to open the web application homepage and Registration section is available"
    tags = "Registration"

    def setup(self):
        self.app = AppFunctions()
        self.host_name = BuiltIn().get_variable_value("${environment.host}")

    def steps(self):
        logger.info(f"Starting test execution, tc_id: {self.tc_id}")
        if self.app.launch_app(self.host_name):
            if self.app.verify_registration_form_visible():
                BuiltIn().pass_execution(f"TC Passed! {self.tc_summary}")
        BuiltIn().fail(f"TC Failed! {self.tc_summary}")

    def teardown(self):
        self.app.quit()


class TC002(object):
    tc_id = "tc_id_002"
    tc_summary = "Verify that user can create a new account when correct details are provided"
    tags = "Registration"

    def setup(self):
        self.host_name = BuiltIn().get_variable_value("${environment.host}")
        self.filename = BuiltIn().get_variable_value("${registration.filename}")
        self.sheet_name = BuiltIn().get_variable_value("${registration.sheet_name}")
        self.tag = BuiltIn().get_variable_value("${registration.happy_flow_tag}")
        self.app = AppFunctions()

    def steps(self):
        logger.info(f"Starting test execution, tc_id: {self.tc_id}")
        if self.app.launch_app(self.host_name):
            if self.app.registration(self.filename, self.sheet_name, self.tag):
                if self.app.verify_account_page_visible():
                    BuiltIn().pass_execution(f"TC Passed! {self.tc_summary}")
        BuiltIn().fail(f"TC Failed! {self.tc_summary}")

    def teardown(self):
        self.app.quit()


class TC003(object):
    tc_id = "tc_id_003"
    tc_summary = "Verify that user can login to application using newly created user account"
    tags = "Registration"

    def setup(self):
        self.host_name = BuiltIn().get_variable_value("${environment.host}")
        self.filename = BuiltIn().get_variable_value("${registration.filename}")
        self.sheet_name = BuiltIn().get_variable_value("${registration.sheet_name}")
        self.tag = BuiltIn().get_variable_value("${registration.happy_flow_tag2}")
        self.app = AppFunctions()
        self.app.launch_app(self.host_name)
        self.user_details = self.app.registration(self.filename, self.sheet_name, self.tag)
        try:
            assert self.user_details, "Unable to create new user, can not proceed ahead with test case"
        except AssertionError:
            BuiltIn().fail(f"TC Failed! {self.tc_summary}")
        self.app.verify_account_page_visible()
        self.app.quit()

    def steps(self):
        logger.info(f"Starting test execution, tc_id: {self.tc_id}")
        self.app = AppFunctions()
        if self.app.launch_app(self.host_name):
            if self.app.login(self.user_details["email"], self.user_details["password"]):
                if self.app.verify_account_page_visible():
                    BuiltIn().pass_execution(f"TC Passed! {self.tc_summary}")
        BuiltIn().fail(f"TC Failed! {self.tc_summary}")

    def teardown(self):
        self.app.quit()


class TC004(object):
    tc_id = "tc_id_004"
    tc_summary = "Verify that user Registration should not be allowed for already created user"
    tags = "Registration"

    def setup(self):
        self.host_name = BuiltIn().get_variable_value("${environment.host}")
        self.filename = BuiltIn().get_variable_value("${registration.filename}")
        self.sheet_name = BuiltIn().get_variable_value("${registration.sheet_name}")
        self.tag = BuiltIn().get_variable_value("${registration.happy_flow_tag3}")
        self.app = AppFunctions()
        self.app.launch_app(self.host_name)
        self.user_details = self.app.registration(self.filename, self.sheet_name, self.tag)
        try:
            assert self.user_details, "Unable to create new user, can not proceed ahead with test case"
        except AssertionError:
            BuiltIn().fail(f"TC Failed! {self.tc_summary}")
        self.app.verify_account_page_visible()
        self.app.quit()

    def steps(self):
        logger.info(f"Starting test execution, tc_id: {self.tc_id}")
        self.app = AppFunctions()
        if self.app.launch_app(self.host_name):
            if self.app.registration(self.filename, self.sheet_name, self.tag) is False:
                BuiltIn().pass_execution(f"TC Passed! {self.tc_summary}")
        BuiltIn().fail(f"TC Failed! {self.tc_summary}")

    def teardown(self):
        self.app.quit()


class TC005(object):
    tc_id = "tc_id_005"
    tc_summary = "Verify that user Registration can not start with invalid email address"
    tags = "Registration"

    def setup(self):
        self.host_name = BuiltIn().get_variable_value("${environment.host}")
        self.filename = BuiltIn().get_variable_value("${registration.filename}")
        self.sheet_name = BuiltIn().get_variable_value("${registration.sheet_name}")
        self.invalid_email = BuiltIn().get_variable_value("${registration.invalid_email}")
        self.app = AppFunctions()

    def steps(self):
        logger.info(f"Starting test execution, tc_id: {self.tc_id}")
        if self.app.launch_app(self.host_name):
            if self.app.create_new_account(self.invalid_email) is False:
                BuiltIn().pass_execution(f"TC Passed! {self.tc_summary}")
        BuiltIn().fail(f"TC Failed! {self.tc_summary}")

    def teardown(self):
        self.app.quit()
