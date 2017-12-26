"""
Copyright 2017 Scott Wiederhold
This file is part of Glowforge-Utilities.

    Glowforge-Utilities is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Glowforge-Utilities is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GF-Library.  If not, see <http://www.gnu.org/licenses/>.


TODO: Error checking/handling of some kind
"""
import ConfigParser


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
    config = ConfigParser.SafeConfigParser(defaults)
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
