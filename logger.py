""" A simple logger abstraction """
__author__ = 'Jego Carlo Ramos'
__copyright__ = 'Copyright 2020, Blackpearl Technology'
__credits__ = ['Jego Carlo Ramos']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Jego Carlo Ramos'
__email__ = 'jego.ramos@blackpearl.technology'
__status__ = 'Development'

import logging
import logging.handlers
import yaml

# Get the config from the ymal file
_logging_config = open("logging_config.yaml")
_config = yaml.load(_logging_config, Loader=yaml.FullLoader)

# TODO: Add more flexibility in terms of filehandlers and formats
# TODO: Also make it pretty
class Logger:
    _codename = None
    _module_name = None

    @classmethod
    def set_codename(cls, codename):
        cls._codename = { 'codename': codename }

    @classmethod
    def set_module_name(cls, name):
        cls._module_name = name
    
    @classmethod
    def get_logger(cls):
        # Enforce _codename value
        if not cls._codename: raise ValueError("You must call set_codename() first")

        # Check if _module_name is passed
        module_name = cls._module_name
        if not cls._module_name:
            module_name = __name__

        # Build the logger
        config = _config
        logger = logging.getLogger(module_name)
        debug_level = getattr(logging, config['dev_logger']['level'])
        logger.setLevel(debug_level)

        formatter = logging.Formatter(config['dev_logger']['format'])

        # add file handler
        file_handler = logging.FileHandler(config['dev_logger']['file_handler']) 
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.codename = cls._codename

        # Add syslog handler
        remote_domain = config['dev_logger']['remote_server_domain']
        remote_port = config['dev_logger']['remote_server_port']
        syslog_handler = logging.handlers.SysLogHandler(address = (remote_domain, remote_port))
        syslog_handler.setFormatter(formatter)
        logger.addHandler(syslog_handler)
        return logging.LoggerAdapter(logger, cls._codename)
