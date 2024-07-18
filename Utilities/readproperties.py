import configparser
import csv


class ReadConfig:
    @staticmethod
    def get_logs_directory():
        config = configparser.ConfigParser()
        config.read('C:/Users/RAMESH SINGH/PycharmProjects/Dash_app/Configuration/config.init')
        return config['DEFAULT']['LogsDirectory']

    @staticmethod
    def get_auth_url():
        config = configparser.ConfigParser()
        config.read('C:/Users/RAMESH SINGH/PycharmProjects/Dash_app/Configuration/config.init')
        return config['authorization']['auth_url']

    @staticmethod
    def get_auth_method():
        config = configparser.ConfigParser()
        config.read('C:/Users/RAMESH SINGH/PycharmProjects/Dash_app/Configuration/config.init')
        return config['authorization']['auth_method']

    @staticmethod
    def get_auth_headers():
        config = configparser.ConfigParser()
        config.read('C:/Users/RAMESH SINGH/PycharmProjects/Dash_app/Configuration/config.init')
        return config['authorization']['auth_headers']

    @staticmethod
    def get_auth_payload():
        config = configparser.ConfigParser()
        config.read('C:/Users/RAMESH SINGH/PycharmProjects/Dash_app/Configuration/config.init')
        return config['authorization']['auth_payload']


    @staticmethod
    def get_csv_file_path():
        config = configparser.ConfigParser()
        config.read('C:/Users/RAMESH SINGH/PycharmProjects/Dash_app/Configuration/config.init')
        return config['DEFAULT']['CSVFilePath']

    @staticmethod
    def get_base_url():
        config = configparser.ConfigParser()
        config.read('C:/Users/RAMESH SINGH/PycharmProjects/Dash_app/Configuration/config.init')
        return config['DEFAULT']['Base_url']

    @staticmethod
    def read_csv(file_path):
        with open(file_path, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            data = [row for row in csv_reader]
        return data
