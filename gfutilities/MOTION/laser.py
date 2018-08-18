"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from . import steps


def find(raw_pulse, on=True):
    """
    Returns pulse where the laser is on or off.
    :param raw_pulse: {str} Raw pulse string to search
    :param on: {bool} True to find on, False to find off.
    :return:
    """
    pulse_number = 0

    for pulse in raw_pulse:
        pulse_number += 1
        decoded_pulse = steps.decode(pulse)
        if (decoded_pulse['LE'] and on) or (not decoded_pulse['LE'] and not on):
            break

    if pulse_number < len(raw_pulse):
        return pulse_number
    else:
        return False


def on_count(raw_pulse):
    """
    Returns count of pulses with the laser on.
    :param raw_pulse: {str} Raw pulse string to search
    :return: {int} Count
    """
    count = 0
    for pulse in raw_pulse:
        decoded_pulse = steps.decode(pulse)
        if decoded_pulse['LE']:
            count += 1
    return count
