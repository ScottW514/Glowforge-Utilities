"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
import collections

n_dict = lambda: collections.defaultdict(n_dict)


def decode(header):
    dec_header = n_dict()
    s = 0
    while s < len(header):
        dec_header[header[s:s+4]] = ord(header[s+4:s+5]) + (ord(header[s+5:s+6]) * 0x100) + \
                                    (ord(header[s+6:s+7]) * 0x10000) + (ord(header[s+7:s+8]) * 0x1000000)
        s += 8
    return dec_header
