"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from typing import NamedTuple, Union

LOGGER_NAME = 'openglow'


class MachineSetting(NamedTuple):
    type: type
    in_report: bool
    min_value: Union[int, None]
    max_value: Union[int, None]
    default: Union[int, str, float, None]
    idle: callable = None
    run: callable = None
    cool_down: callable = None


__all__ = [
    # Constants
    'LOGGER_NAME',

    # Named Tuples
    'MachineSetting',
]
