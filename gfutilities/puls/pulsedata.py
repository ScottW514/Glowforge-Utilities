"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
_decode_step_codes = {
    'LE': {'mask': 0b00010000, 'test': 0b00010000},  # Laser Enable (ON)
    'LP': {'mask': 0b10000000, 'test': 0b01111111},  # Laser Power Setting
    'XP': {'mask': 0b00000011, 'test': 0b00000001},  # X+ Step
    'XN': {'mask': 0b00000011, 'test': 0b00000011},  # X- Step
    'YN': {'mask': 0b00001100, 'test': 0b00000100},  # Y- Step
    'YP': {'mask': 0b00001100, 'test': 0b00001100},  # Y+ Step
    'ZP': {'mask': 0b01100000, 'test': 0b00100000},  # Z+ Step
    'ZN': {'mask': 0b01100000, 'test': 0b01100000},  # Z- Step
}

_SPEED = 1000


def decode_all_steps(puls: bytes, data: dict = None, mode: tuple = (8, 2)) -> dict:
    cnt = {
        'XP': 0,
        'XN': 0,
        'XTOT': 0,
        'XEND': 0,
        'YP': 0,
        'YN': 0,
        'YTOT': 0,
        'YEND': 0,
        'ZP': 0,
        'ZN': 0,
        'ZTOT': 0,
        'ZEND': 0,
        'LE': 0,
        'LP': 0,
    }
    for step in puls:
        if step & _decode_step_codes['LP']['mask']:
            # Power Setting (LP)
            cnt['LP'] = cnt['LP'] + 1
        else:
            for action in sorted(_decode_step_codes):
                if not (step & _decode_step_codes[action]['mask']) ^ _decode_step_codes[action]['test']:
                    cnt[action] = cnt[action] + 1
                    if action != 'LE':
                        cnt[action[0:1] + 'TOT'] = cnt[action[0:1] + 'TOT'] + 1
                        cnt[action[0:1] + 'END'] = cnt[action[0:1] + 'END'] + 1 \
                            if action[1:2] == 'P' else cnt[action[0:1] + 'END'] - 1

    for axis in ('X', 'Y'):
        cnt[axis + 'MM'] = (cnt[axis + 'END'] / mode[0]) * 0.15
    cnt['ZMM'] = (cnt['ZEND'] / mode[1]) * 0.70612

    for axis in ('X', 'Y', 'Z'):
        cnt[axis + 'IN'] = cnt[axis + 'MM'] / 25.4

    if data is not None:
        for key, val in cnt.items():
            cnt[key] = val + data.get(key, 0)
    return cnt
