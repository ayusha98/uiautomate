import os
from robot import rebot
from robot.libraries.BuiltIn import BuiltIn
from config_parser import ConfigParser


class loadconfig(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, confpath, filename, lib_pth, result_pth, tmp_pth, mail, output_dir):
        self.globalconfigDict = ConfigParser(confpath, filename).parse_config()
        self.cfg_filename = filename
        self.lib_pth = lib_pth
        self.conf_pth = confpath
        self.result_pth = result_pth
        self.tmp_pth = tmp_pth
        self.output_dir = output_dir
        self.send_mail = True if eval(mail) else False
        self.suite_name = os.path.basename(self.output_dir).split('_')[0]

    def start_suite(self, name, attrs):
        self.__set_variables()

    def start_test(self, name, attrs):
        self.__set_variables()

    def end_test(self, name, attrs):
        pass

    def end_suite(self, name, attrs):
        pass

    def close(self):
        rebot("%s/output.xml" % self.output_dir, outputdir=self.output_dir,
              reportbackground="lightgreen:#F9DA40:#F9DA40")
        # TODO: we can send this report over email

    def __set_variables(self):
        for key in self.globalconfigDict:
            BuiltIn().set_global_variable(f"${key}", self.globalconfigDict[key])

        BuiltIn().set_global_variable("${lib_pth}", self.lib_pth)
        BuiltIn().set_global_variable("${conf_pth}", self.conf_pth)
        BuiltIn().set_global_variable("${result_pth}", self.result_pth)
        BuiltIn().set_global_variable("${tmp_pth}", self.tmp_pth)

        self.output_dir = BuiltIn().get_variable_value("${OUTPUT DIR}")
        self.suite_name = BuiltIn().get_variable_value("${SUITE NAME}")
        self.report_file = BuiltIn().get_variable_value("${REPORT FILE}")
        if self.send_mail:
            self.mail_to = BuiltIn().get_variable_value("${reporting.email}")
