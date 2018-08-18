"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def parse(cfg_file):
    """
    Parses configuration file and returns dict object with values as: <SECTION>.<PARAM>: value.
    Note: SECTION and PARAM are converted to uppercase.
    :param cfg_file: {str} path to configuration file
    :return: {dict} Configuration parameter values
    """
    defaults = {
        'log_level': 'DEBUG',
        'console_log_level': 'False',
    }
    cfg = {}
    config = configparser.SafeConfigParser(defaults)
    config.read(cfg_file)
    for section in config.sections():
        for item in config.items(section):
            if item[1] == 'True':
                value = True
            elif item[1] == 'False':
                value = False
            else:
                value = item[1]
            cfg['%s.%s' % (str.upper(section), str.upper(item[0]))] = value
    return cfg
