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
    along with Glowforge-Utilities.  If not, see <http://www.gnu.org/licenses/>.


TODO: Error checking/handling of some kind
"""
from . import _REPORTED_SETTINGS, _MOTION_SETTINGS
import time


def report(cfg):
    """
    Generate device settings report
    :param cfg: {dict} Emulator's configuration dictionary
    :return: {str} String formatted for setting report
    """
    settings = ''
    value = ''
    for item in sorted(_REPORTED_SETTINGS):
        if isinstance(_REPORTED_SETTINGS[item], dict):
            if 'cfg' in _REPORTED_SETTINGS[item]:
                value = cfg[_REPORTED_SETTINGS[item]['cfg']]
                if isinstance(_REPORTED_SETTINGS[item]['type'], str):
                    value = '"%s"' % value
            elif 'data' in _REPORTED_SETTINGS[item]:
                if _REPORTED_SETTINGS[item]['data'] == 'epoch':
                    value = int(time.time())
            else:
                value = 0
        else:
            if isinstance(_REPORTED_SETTINGS[item], str):
                value = '"%s"' % _REPORTED_SETTINGS[item]
            else:
                value = _REPORTED_SETTINGS[item]
        settings += '"%s":%s,' % (item, value)
    return '{%s}' % settings[:-1]


def decode_motion(header):
    settings = {}
    for item in header:
        if item in _MOTION_SETTINGS:
            if _MOTION_SETTINGS[item] is not None:
                settings[_MOTION_SETTINGS[item]] = header[item]
    return settings
