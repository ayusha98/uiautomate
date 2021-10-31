import os
import configparser
from logger import Logger
from xlrd import open_workbook, XLRDError


class ConfigParser(object):
    def __init__(self, conf_path, conf_file_name):
        self.logger = Logger.__call__().get_logger()
        self.conf_file_name = os.path.join(conf_path, conf_file_name)
        self.conf_dict = {}
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file_name)

    def parse_config(self):
        """
        Return the dictionary format, key:value pair for each section's config attributes
        Notation used: section.key_name=value. E.g.: reporting.email = ayusha98@gmail.com
        """

        self.logger.debug(f"parse_config, config file name: {self.conf_file_name}")
        sections_list = self.config.sections()
        for section in sections_list:
            for (key, value) in self.config.items(section):
                self.conf_dict[f"{section}.{key}"] = value
        return self.conf_dict


class ParseXLS(object):
    def __init__(self, xls_path, xls_file_name):
        self.logger = Logger.__call__().get_logger()
        self.xls_file_name = os.path.join(xls_path, xls_file_name)
        self.data_dict = {}

    def main(self, sheet_name):
        """
        This function will return list of dictionary, where the dictionary keys are top row's header values
        We can uniquely identify different rows using 'tag' column
        """

        self.logger.debug(f"parse_xls, xls file name: {self.xls_file_name}")
        wb = open_workbook(self.xls_file_name)
        sheet_list = []
        try:
            sheet = wb.sheet_by_name(sheet_name)
        except XLRDError as e:
            logger.error(f"Invalid sheet name: {sheet_name}\nException: {e}")
            sys.exit(1)

        keys_list = [sheet.cell_value(0, each_col) for each_col in range(sheet.ncols)]
        for each_row in range(1, sheet.nrows):
            row_dict = {}
            for index, each_col in enumerate(range(sheet.ncols)):
                cell_value = str(sheet.cell_value(each_row, each_col))
                row_dict[keys_list[index]] = cell_value
            sheet_list.append(row_dict)
        del wb
        return sheet_list
