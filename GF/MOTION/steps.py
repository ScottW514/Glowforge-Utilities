"""
Copyright 2017 Scott Wiederhold
This file is part of Glowforge-Utilities.

    GF-Library is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GF-Library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GF-Library.  If not, see <http://www.gnu.org/licenses/>.


TODO: Error checking/handling of some kind
"""
_decode_step_codes = {
    'LE': {'mask': 0b00010000, 'test': 0b00010000},  # Laser Enable (ON)
    'XP': {'mask': 0b00000011, 'test': 0b00000001},  # X+ Step
    'XN': {'mask': 0b00000011, 'test': 0b00000011},  # X- Step
    'YP': {'mask': 0b00001100, 'test': 0b00000100},  # Y+ Step
    'YN': {'mask': 0b00001100, 'test': 0b00001100},  # Y- Step
    'ZP': {'mask': 0b01100000, 'test': 0b00100000},  # Z+ Step
    'ZN': {'mask': 0b01100000, 'test': 0b01100000},  # Z- Step
}


def decode_step(step):
    global _decode_step_codes
    step_actions = {}
    if step & 0b10000000:
        # Power Setting (LP)
        step_actions['LP'] = step & 0b01111111
    else:
        for action in sorted(_decode_step_codes):
            # Non Power Setting - Check for actions
            step_actions[action] = \
                False if (step & _decode_step_codes[action]['mask']) ^ _decode_step_codes[action]['test'] else True

    return step_actions
