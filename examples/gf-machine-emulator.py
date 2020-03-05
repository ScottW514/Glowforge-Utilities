#!/usr/bin/python
"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from gfutilities import ServiceConnector, Emulator

machine = Emulator()

service = ServiceConnector('gf-machine-emulator.cfg', machine)
service.connect()
service.run()
