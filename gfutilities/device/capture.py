"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from threading import Thread
import time
import logging


class Capture(Thread):
    """
    Capture Message Queue
    Responds to incoming WSS events to capture images from the onboard cameras.
    """
    def __init__(self, machine: 'BaseMachine'):
        """
        Initialize Capture Dispatcher
        :param machine: Machine object
        :type machine: BaseMachine
        """
        self.machine = machine
        self.stop = False
        Thread.__init__(self)

    def run(self) -> None:
        logging.debug('THREAD START')
        while not self.stop:
            if not self.machine.capture_q.empty():
                (s, q, msg) = self.machine.capture_q.get()
                if msg['action_type'] == 'lid_image':
                    self.machine.lid_image(s=s, q=q, msg=msg)
                elif msg['action_type'] == 'head_image':
                    self.machine.head_image(s=s, q=q, msg=msg)
                elif msg['action_type'] == 'lidar_image':
                    self.machine.lidar_image(s=s, q=q, msg=msg)
                self.machine.capture_q.task_done()
            time.sleep(.1)
        logging.debug('THREAD EXIT')
