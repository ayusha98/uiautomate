from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from lib.app_functions import AppFunctions


class TC001(object):
    tc_id = "tc_id_001"
    tc_summary = "Verify that user can open the web application"
    tags = "Registration"

    def setup(self):
        self.app = AppFunctions()
        self.host_name = BuiltIn().get_variable_value("${environment.host}")

    def steps(self):
        logger.info(f"Starting test execution, tc_id: {self.tc_id}")
        if self.app.launch_app(self.host_name):
            BuiltIn().pass_execution(f"Successfully verified that user can open the web application.")
        BuiltIn().fail(f"TC Failed! {self.tc_summary}")

    def teardown(self):
        self.app.quit()


class TC002(object):
    tc_id = "tc_id_002"
    tc_summary = "Verify that user can create an account, when correct details are provided"
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
                BuiltIn().pass_execution(f"Successfully verified that user create an account with valid details")
        BuiltIn().fail(f"TC Failed! {self.tc_summary}")

    def teardown(self):
        self.app.quit()
