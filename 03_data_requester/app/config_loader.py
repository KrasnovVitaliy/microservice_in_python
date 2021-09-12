import os

from singleton import MetaSingleton
from configloader import ConfigLoader

config_abs_path = "/".join(os.path.abspath(__file__).split('/')[0:-1])


class Config(metaclass=MetaSingleton):
    def __init__(self, config_file_path=f'{config_abs_path}/config.yml'):
        self.config_loader = ConfigLoader()
        self.config_loader.update_from_yaml_file(config_file_path)
        self.config_loader.update_from_env_namespace('DATA_REQUESTER')

    def get(self, setting_name):
        return self.config_loader.get(setting_name, None)

    def to_dict(self):
        loader = self.config_loader
        return {key: loader.get(key) for key in loader.keys()}


LOGGING_LEVEL = "LOGGING_LEVEL"
LOGGING_FORMAT = "LOGGING_FORMAT"
WEB_HOST = "WEB_HOST"
WEB_PORT = "WEB_PORT"
BASE_URL = "BASE_URL"
KAFKA_BROKER = "KAFKA_BROKER"
SRC_DATA_TOPIC = "SRC_DATA_TOPIC"
PROMETHEUS_PORT = "PROMETHEUS_PORT"
