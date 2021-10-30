from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger


class TC001(object):
    tc_id = "tc_id_001"
    tc_summary = "Validate the registration page is loaded or not"
    tags = "Registration"

    def setup(self):
        self.host_name = BuiltIn().get_variable_value("${environment.host}")

    def steps(self):
        logger.info(f"Host name: {self.host_name}")

    def teardown(self):
        pass
