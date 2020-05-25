import logging

class LogConfig:
    def set_logging_config(file_name):
        logging.basicConfig(filename=file_name, level=logging.DEBUG)
