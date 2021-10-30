import os
import configparser


class ConfigParser(object):
    def __init__(self, conf_path, conf_file_name):
        self.conf_file_name = os.path.join(conf_path, conf_file_name)
        self.conf_dict = {}
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file_name)

    def parse_config(self):
        sections_list = self.config.sections()
        for section in sections_list:
            for (key, value) in self.config.items(section):
                self.conf_dict[f"{section}.{key}"] = value
        return self.conf_dict
