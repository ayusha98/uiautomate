"""
Test suite/case runner script, see below example
* Run a full test suite :
python3 runner.py <SUITE_NAME> config=<CONFIG>
python3 runner.py suites/Regression config=regression.cfg

* Run a single test file :
python3 runner.py suites/registration.py config=practice.cfg
"""

import os
import ast
import sys
import time
import inspect
import importlib
from robot.api import TestSuite


class Runner(object):
    def get_all_paths(self):
        """
        Resolve all directory paths, add to sys.path
        :return: return a tuple of all directory path
        """

        for i in range(20):
            current_dir = os.getcwd()
            if os.path.basename(current_dir).find("uiautomate") != -1:
                conf_pth = f"{current_dir}/conf"
                sys.path.append(conf_pth)
                lib_pth = f"{current_dir}/lib"
                sys.path.append(lib_pth)
                result_pth = f"{current_dir}/results"
                sys.path.append(result_pth)
                tmp_pth = f"{current_dir}/tmp"
                sys.path.append(tmp_pth)
                return conf_pth, lib_pth, result_pth, tmp_pth
            elif i == 9:
                print("Not able to get conf dir in uiautomate, exiting....")
                sys.exit(1)
            else:
                print(f"Retrying: {10-i} times left")
                os.chdir("..")
        return False

    def parse_test_data(self, suite_obj, suite_name_with_path, only_tc_to_run):
        if suite_name_with_path[-2:] == "py":
            suite_name_no_ext = os.path.basename(suite_name_with_path)[:-3]
        else:
            suite_name_no_ext = os.path.basename(suite_name_with_path)

        suite = suite_obj     # TestSuite(suite_name_no_ext) -- Robot's TestSuite Instance
        with open(suite_name_with_path) as f:
            node = ast.parse(f.read())
        root_node = os.path.dirname(suite_name_with_path)
        if not os.path.exists(f"{root_node}/__init__.py"):
            with open(f"{root_node}/__init__.py", 'w'):
                pass

        # load all the classes in the py file
        all_tc_classes = [x.name for x in [n for n in node.body if isinstance(n, ast.ClassDef)]]

        if only_tc_to_run and len(only_tc_to_run) > 0:
            test_cases_to_run = [x for x in only_tc_to_run if x in all_tc_classes]
            if test_cases_to_run == only_tc_to_run:
                all_tc_classes = test_cases_to_run
            else:
                print("Specified tc did not match with TestCases in file, Executing all TestCases..")

        # remove duplicate test cases (if specified multiple times)
        all_tc_classes = [i for n, i in enumerate(all_tc_classes) if i not in all_tc_classes[:n]]

        multi_level_suite = False
        tmp_path = suite_name_with_path.replace("suites/", "")
        if tmp_path.find("/") != -1:
            multi_level_suite = True
            temp_suite_name_str = suite_name_with_path.split("/")
            main_suite = f'{(".".join(temp_suite_name_str[:-1]))}'
            child_suite = temp_suite_name_str[-1][:-3]
        if multi_level_suite:
            for tc in all_tc_classes:
                suite.resource.imports.library(f"{main_suite}.{child_suite}.{tc}")
        else:
            for tc in all_tc_classes:
                suite.resource.imports.library(f"suites.{suite_name_no_ext}.{tc}")

        for tc in all_tc_classes:
            if multi_level_suite:
                sys.path.append(os.path.join(os.getcwd(), os.path.dirname(suite_name_with_path)))
            else:
                sys.path.append(os.path.join(os.getcwd(), 'suites'))
            module = importlib.import_module(suite_name_no_ext)
            for name, class_obj in inspect.getmembers(module):
                if inspect.isclass(class_obj) and class_obj.__module__ == suite_name_no_ext and name == tc:
                    tc_class_obj = class_obj

            try:
                real_test_name_raw = tc_class_obj.tc_summary
                real_test_id_raw = tc_class_obj.tc_id
                real_tags_raw = tc_class_obj.tags
            except AttributeError:
                print(f"{'*'*50}\n\nERROR: Invalid Test case, tc_id/tags/tc_summary "
                      f"missing from test case: {tc}\n\n{'*'*50}")
                sys.exit(1)

            if multi_level_suite:
                main_child_suite = "%s.%s" % (main_suite, child_suite)
                suite_index = main_child_suite.split(".").index(suite.name)+1
                test_suite_parent = ".".join(main_child_suite.split(".")[suite_index:])
                real_test_name = f"{test_suite_parent}.{tc} {real_test_id_raw.strip()}:{real_test_name_raw.strip()}"
            else:
                real_test_name = f"{tc} {real_test_id_raw.strip()}:{real_test_name_raw.strip()}"

            real_tags = real_tags_raw.strip()
            tag_list = [tag.strip() for tag in real_tags.split(",")]
            test = suite.tests.create(real_test_name, tags=tag_list)

            # we need to uniquely identify each test case, across whole test suite
            if multi_level_suite:
                test.setup.name = f"{main_suite}.{child_suite}.{tc}.setup"
                test.body.create_keyword(f"{main_suite}.{child_suite}.{tc}.steps")
                test.teardown.name = f"{main_suite}.{child_suite}.{tc}.teardown"
            else:
                test.setup.name = f"suites.{suite_name_no_ext}.{tc}.setup"
                test.body.create_keyword(f"suites.{suite_name_no_ext}.{tc}.steps")
                test.teardown.name = f"suites.{suite_name_no_ext}.{tc}.teardown"
        return suite, {suite_name_no_ext: all_tc_classes}

    def add_to_dict(self, target_dict, dict_key, dict_value):
        if dict_key in target_dict:
            value = target_dict[dict_key]
            value.append(dict_value)
            target_dict[dict_key] = value
        else:
            target_dict[dict_key] = [dict_value]
        return target_dict

    def parse_directory(self, path):
        if not path.endswith(os.sep):
            path = path + os.sep

        tc_py_files = []
        for root, directory, files in os.walk(path):
            for tc_file in files:
                if tc_file.endswith(".py") and '__init__' not in tc_file:
                    tc_py_files.append(os.path.join(root, tc_file))

        directory_tc_dict = {}
        for tc_file in tc_py_files:
            if os.path.dirname(tc_file) + os.sep == path:
                directory_tc_dict = self.add_to_dict(directory_tc_dict, path, tc_file)
        return directory_tc_dict

    def run(self):
        """
        Main function for the Runner class,
        1. It will parse the test suite / file and resolve the test cases (python classes)
        2. Start the TestSuite instance and call parse_test_data function to add the test cases in it
        3. Call TestSuite.run function along with listener class : loadconfig -- this will start execution of the Suite
        """

        conf_pth, lib_pth, result_pth, tmp_pth = self.get_all_paths()
        config_file = False

        arg_list = sys.argv[1:]
        for arg in arg_list:
            if 'config=' in arg:
                config_file = arg.split("=")[1].split(",")[0]
                arg_list.remove(arg)
        if not config_file:
            print(f"ERROR: No config file provided, can not proceed with suite execution. Exiting..'")
            return False

        suite_name_with_path = arg_list[0]
        suite_name = os.path.basename(suite_name_with_path)

        # if we want to specify the test case in command line i.e. tc=tc1,tc2
        specific_tc_to_run = []
        for arg in arg_list:
            if 'tc=' in arg:
                specific_tc_to_run = arg.split("=")[1].split(",")

        if len(suite_name.strip()) == 0:
            suite_name = os.path.basename(suite_name_with_path.strip("/"))
        output_dir = f'{result_pth}/{suite_name}_{time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time()))}'

        # suite name could be a single python file or the directory (full test suite)
        if suite_name[-3:] == ".py":
            suite_name_no_ext = suite_name[:-3]
            suite_obj = TestSuite(suite_name_no_ext)
            suite, file_tc_dict = self.parse_test_data(suite_obj, suite_name_with_path, specific_tc_to_run)
            suite.run(loglevel="TRACE", debugfile="debug.txt", outputdir=output_dir,
                      listener=f'loadconfig:{conf_pth}:{config_file}:{lib_pth}:{result_pth}:{tmp_pth}:{output_dir}')
            return output_dir
        else:
            suite = TestSuite(suite_name)
            directory_tc_dict = self.parse_directory(suite_name_with_path.strip("/"))
            directory_path = list(directory_tc_dict.keys())[0]

            # let's just be safe, create __init__.py if not already present
            if not os.path.exists("suites/__init__.py"):
                with open("suites/__init__.py", 'w'):
                    pass

            if not os.path.exists(f"{directory_path}/__init__.py"):
                with open(f"{directory_path}/__init__.py", 'w'):
                    pass

            tc_files = directory_tc_dict[directory_path]
            tc_files.sort()
            for tc_file in tc_files:
                suite, file_tc_dict = self.parse_test_data(suite, tc_file, specific_tc_to_run)

            suite.run(loglevel="TRACE", debugfile="debug.txt", outputdir=output_dir,
                      listener=f'loadconfig:{conf_pth}:{config_file}:{lib_pth}:{result_pth}:{tmp_pth}:{output_dir}')
            return output_dir


if __name__ == '__main__':
    Runner().run()
