"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import configparser
import logging
from typing import Any

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


def log_level(level_str: str) -> int:
    """
    Returns logging log level object based on provided string.
    :param level_str: Desired logging level
    :type level_str: str
    :return: Logging level object
    :rtype: int
    """
    levels = {
        'CRITICAL': logging.CRITICAL, 'ERROR': logging.ERROR, 'WARNING': logging.WARNING, 'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }
    if level_str in levels:
        return levels[level_str]
    else:
        return logging.INFO


def get_cfg(parameter: str) -> Any:
    """
    Returns value of configuration parameter
    :param parameter: Parameter to return
    :type parameter: str
    :return: The value of the parameter
    :rtype: Any
    """
    return _CONFIG.get(parameter)


def set_cfg(parameter: str, value: Any, keep_value: bool = False):
    """
    Returns value of configuration parameter
    :param parameter: Parameter to set
    :type parameter: str
    :param value: Value of parameter
    :type value: Any
    :param keep_value: Keep existing value if set
    :type keep_value: bool
    """
    if keep_value and get_cfg(parameter) is not None:
        return
    _CONFIG[parameter] = value


__all__ = ['get_cfg', 'parse', 'set_cfg', 'log_level']
