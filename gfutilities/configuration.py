"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from typing import Any
import configparser

_CONFIG = {}


def parse(cfg_file: str) -> None:
    """
    Parses configuration file and returns dict object with values as: <SECTION>.<PARAM>: value.
    Note: SECTION and PARAM are converted to uppercase.
    :param cfg_file: path to configuration file
    :type cfg_file: str
    """
    defaults = {
        'log_level': 'DEBUG',
        'console_log_level': 'False',
    }
    config = configparser.ConfigParser(defaults)
    config.read(cfg_file)
    for section in config.sections():
        for item in config.items(section):
            if item[1] == 'True':
                value = True
            elif item[1] == 'False':
                value = False
            else:
                value = item[1]
            _CONFIG['%s.%s' % (str.upper(section), str.upper(item[0]))] = value


def get_cfg(parameter: str) -> Any:
    """
    Returns value of configuration parameter
    :param parameter: Parameter to return
    :type parameter: str
    :return: The value of the parameter
    :rtype: Any
    """
    return _CONFIG.get(parameter)


def set_cfg(parameter: str, value: Any):
    """
    Returns value of configuration parameter
    :param parameter: Parameter to set
    :type parameter: str
    :param value: Value of parameter
    :type value: Any
    """
    _CONFIG[parameter] = value
