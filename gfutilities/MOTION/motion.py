"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from . import header
from gfutilities.SETTINGS import settings


class Motion:
    def __init__(self, mfile):
        """
        Initial Class
        :param mfile: Motion file to load
        """
        self.raw_header = ''
        self.raw_pulse = ''
        self._load_file(mfile)
        self.header = header.decode(self.raw_header)
        self.settings = settings.decode_motion(self.header)
        self.pulse_total = len(self.raw_pulse)
        self.pulse_current = 1
        self.position_current = {'X': 0, 'Y': 0, 'Z': 0}
        self.source_file = mfile

    def _load_file(self, mfile):
        """
        Loads motion file
        :param mfile: Motion file to load
        :return:
        """
        with open(mfile, 'rb') as f:
            f.seek(1)
            if f.read(3).decode('UTF-8') != 'GF1':
                # This isn't a GF1 pulse file.
                return False
            head_len = ord(f.read(1)) + (ord(f.read(1)) * 256)
            f.read(2)
            self.raw_header = f.read(head_len - 8)
            self.raw_pulse = f.read()
        return True
