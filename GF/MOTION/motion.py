"""
Copyright 2017 Scott Wiederhold
This file is part of GF-Library.

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
from .header import decode_header
from ..SETTINGS.settings import decode_motion_settings


class Motion:
    def __init__(self, mfile):
        """
        Initial Class
        :param mfile: Motion file to load
        """
        self._load_file(mfile)
        self.header = decode_header(self.raw_header)
        self.settings = decode_motion_settings(self.header)
        self.total_steps = len(self.raw_pulse)
        self.cur_position = {'X': 0, 'Y': 0, 'Z': 0}

    def _load_file(self, mfile):
        """
        Loads motion file
        :param mfile: Motion file to load
        :return:
        """
        with open(mfile, 'rb') as f:
            f.seek(1)
            if f.read(3) != 'GF1':
                # This isn't a GF1 pulse file.
                return False
            head_len = ord(f.read(1)) + (ord(f.read(1)) * 256)
            f.read(2)
            self.raw_header = f.read(head_len - 8)
            self.raw_pulse = f.read()
        return True
