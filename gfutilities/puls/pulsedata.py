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


def generate_linear_puls(x: int, y: int, outfile: str) -> None:
    expected_count = abs(x) if abs(x) >= abs(y) else abs(y)

    max_speed = 5
    min_speed = 55
    acc = 10
    acc_dist = int((min_speed - max_speed) / acc)
    acc_dist = acc_dist if acc_dist < (expected_count / 2) else int(expected_count / 2)

    steps = 0
    d = min_speed

    with open(outfile, 'bw') as f:
        for xs, ys in _step_gen(x, y):
            steps += 1
            s = 0
            if xs != 0:
                s |= 0b00000001 if xs > 0 else 0b00000011
            if ys != 0:
                s |= 0b00001100 if ys > 0 else 0b00000100
            f.write(bytes([s]))

            if steps <= acc_dist:
                # Accelerating
                d = d - acc if d > max_speed - acc else max_speed
            elif steps >= (expected_count - acc_dist):
                # Decelerating
                d = d + acc if d < min_speed + acc else min_speed
            f.write('\0'.encode() * d)


def _step_gen(x: int, y: int) -> tuple:
    xd = 1 if x >= 0 else -1
    yd = 1 if y >= 0 else -1
    xt = abs(x)
    yt = abs(y)

    if xt >= yt:
        maj_target = xt
        min_target = yt
        maj_dir = xd
        min_dir = yd
    else:
        maj_target = yt
        min_target = xt
        maj_dir = yd
        min_dir = xd
    if min_target > 0:
        maj_per_min = round(maj_target / min_target, 4)
    else:
        maj_per_min = maj_target

    maj_cnt = 0
    min_cnt = 0
    while maj_cnt < maj_target or min_cnt < min_target:
        if maj_cnt < maj_target:
            maj_cnt += 1
            if maj_cnt % maj_per_min < 1 and min_cnt < min_target:
                min_out = min_dir
                min_cnt += 1
            else:
                min_out = 0
        else:
            maj_dir = 0
            min_out = min_dir
            min_cnt += 1

        yield maj_dir if xt >= yt else min_out, min_out if xt >= yt else maj_dir
