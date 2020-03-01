#!/usr/bin/python
"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from gfutilities.DEVICE.emulator import Emulator

gf = Emulator('examples/gf-machine-emulator.cfg')
gf.connect()
gf.run()
