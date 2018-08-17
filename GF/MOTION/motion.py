"""
Copyright 2018 Scott Wiederhold
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
from . import header
from GF.SETTINGS import settings


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
            if f.read(3) != 'GF1':
                # This isn't a GF1 pulse file.
                return False
            head_len = ord(f.read(1)) + (ord(f.read(1)) * 256)
            f.read(2)
            self.raw_header = f.read(head_len - 8)
            self.raw_pulse = f.read()
        return True
