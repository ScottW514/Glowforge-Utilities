"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

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
