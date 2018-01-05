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
