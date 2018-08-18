"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

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
