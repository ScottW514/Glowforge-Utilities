"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""


class PulseData:
    def __init__(self, mfile):
        """
        Initialize Class
        :param mfile: PulseData file to load
        """
        self.raw_pulse: bytes = b''
        self.header: dict = {}
        self._load_file(mfile)
        self.pulse_total: int = len(self.raw_pulse)
        self.pulse_current: int = 1
        self.position_current: dict = {'X': 0, 'Y': 0, 'Z': 0}
        self.source_file: str = mfile

    def _load_file(self, mfile: str) -> bool:
        """
        Loads motion file
        :param mfile: path to PulseData file to load
        :type mfile: str
        :return: Status of load
        :rtype: bool
        """
        with open(mfile, 'rb') as f:
            f.seek(1)
            if f.read(3).decode('UTF-8') != 'GF1':
                # This isn't a GF1 pulse file.
                return False
            head_len = ord(f.read(1)) + (ord(f.read(1)) * 256)
            f.read(2)
            raw_header = f.read(head_len - 8)
            s = 0
            while s < len(raw_header):
                self.header[raw_header[s:s + 4].decode()] = ord(raw_header[s + 4:s + 5]) + \
                                                    (ord(raw_header[s + 5:s + 6]) * 0x100) + \
                                                    (ord(raw_header[s + 6:s + 7]) * 0x10000) + \
                                                    (ord(raw_header[s + 7:s + 8]) * 0x1000000)
                s += 8
            self.raw_pulse = f.read()
        return True
