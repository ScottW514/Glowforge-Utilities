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
_decode_step_codes = {
    'LE': {'mask': 0b00010000, 'test': 0b00010000},  # Laser Enable (ON)
    'LP': {'mask': 0b10000000, 'test': 0b01111111},  # Laser Power Setting
    'XP': {'mask': 0b00000011, 'test': 0b00000001},  # X+ Step
    'XN': {'mask': 0b00000011, 'test': 0b00000011},  # X- Step
    'YP': {'mask': 0b00001100, 'test': 0b00000100},  # Y+ Step
    'YN': {'mask': 0b00001100, 'test': 0b00001100},  # Y- Step
    'ZP': {'mask': 0b01100000, 'test': 0b00100000},  # Z+ Step
    'ZN': {'mask': 0b01100000, 'test': 0b01100000},  # Z- Step
}


def decode(raw_step):
    """
    Decodes raw steps
    :param raw_step: {str} Binary representation of step
    :return: {dict} Decoded step dictionary in format of _decode_step_codes, or LP
    """
    global _decode_step_codes
    step = ord(raw_step)
    step_actions = {}
    if step & _decode_step_codes['LP']['mask']:
        # Power Setting (LP)
        step_actions['LP'] = step & _decode_step_codes['LP']['test']
        step = 0
    for action in sorted(_decode_step_codes):
        if action != 'LP':
            # Check for Non-Power actions
            step_actions[action] = \
                False if (step & _decode_step_codes[action]['mask']) ^ _decode_step_codes[action]['test'] else True

    return step_actions


def find(raw_pulse, search_axis=None, direction=None):
    """
    Returns pulse number with first occurrence of step
    :param raw_pulse: {
    :param search_axis: (str) Which axis to look for pulse from ('X','Y','Z'). Defaults to any.
    :param direction: (bool) True for positive, False for negative. Defaults to None for any.
    :return: {int} pulse number, or False if not found
    """
    axis_list = ['X', 'Y', 'Z']

    if search_axis is None:
        search_axis = axis_list
    else:
        search_axis = [search_axis]

    pulse_number = 0
    step_found = False

    for pulse in raw_pulse:
        if step_found:
            break
        pulse_number += 1
        decoded_pulse = decode(pulse)
        for axis in search_axis:
            if (decoded_pulse[axis + 'P'] and (direction is None or direction)) or \
                    (decoded_pulse[axis + 'N'] and (direction is None or not direction)):
                step_found = pulse_number

    return step_found
