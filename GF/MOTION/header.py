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
    along with GF-Library.  If not, see <http://www.gnu.org/licenses/>.


TODO: Error checking/handling of some kind
"""
import collections

n_dict = lambda: collections.defaultdict(n_dict)


def decode_header(header):
    dec_header = n_dict()
    s = 0
    while s < len(header):
        dec_header[header[s:s+4]] = ord(header[s+4:s+5]) + (ord(header[s+5:s+6]) * 0x100) + \
                                    (ord(header[s+6:s+7]) * 0x10000) + (ord(header[s+7:s+8]) * 0x1000000)
        s += 8
    return dec_header
