#!/usr/bin/python
"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from gfutilities.DEVICE.emulator import Emulator

gf = Emulator('examples/gf-machine-emulator.cfg')
gf.connect()
gf.run()
