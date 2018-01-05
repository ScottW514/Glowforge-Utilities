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


def delta(raw_pulse):
    """
    Finds change in X,Y,Z position as result of raw_pulse str.
    :param raw_pulse: {str} Raw pulse string
    :return: {dict} Dictionary contain indexes 'X', 'Y', 'Z' with step counts as {int}
    """
    position_delta = {'X': 0, 'Y': 0, 'Z': 0}
    for pulse in raw_pulse[0:len(raw_pulse)]:
        dec_pulse = steps.decode(pulse)
        for axis in position_delta:
            if dec_pulse[axis + 'P']:
                position_delta[axis] += 1
            elif dec_pulse[axis + 'N']:
                position_delta[axis] -= 1
    return position_delta


def extents(raw_pulse):
    """
    Finds maximum X, Y, and Z extents from 0
    :param raw_pulse: {str} Raw pulse string
    :return: {dict} Dictionary contain indexes 'XP|N', 'YP|N', 'ZP|N' with max step counts as {int}
    """
    axis_list = ['X', 'Y', 'Z']
    axis_extents = {'XP': 0, 'YP': 0, 'ZP': 0, 'XN': 0, 'YN': 0, 'ZN': 0}
    position = {'X': 0, 'Y': 0, 'Z': 0}

    for pulse in raw_pulse:
        dec_pulse = steps.decode(pulse)
        for axis in axis_list:
            if dec_pulse[axis + 'P']:
                position[axis] += 1
            if dec_pulse[axis + 'N']:
                position[axis] -= 1
            if position[axis] > 0 and position[axis] > axis_extents[axis + 'P']:
                axis_extents[axis + 'P'] = position[axis]
            elif position[axis] < 0 and position[axis] < axis_extents[axis + 'N']:
                axis_extents[axis + 'N'] = position[axis]
    return axis_extents
