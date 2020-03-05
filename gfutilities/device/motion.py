"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from threading import Thread
import time
import logging


class Motion(Thread):
    """
    Motion Message Queue
    Responds to incoming WSS events for motion actions..
    """
    def __init__(self, machine: 'BaseMachine'):
        """
        Initialize Motion Dispatcher
        :param machine: Machine object
        :type machine: BaseMachine
        """
        self.machine = machine
        self.stop = False
        Thread.__init__(self)

    def run(self) -> None:
        logging.debug('THREAD START')
        while not self.stop:
            if not self.machine.motion_q.empty():
                (s, q, msg) = self.machine.motion_q.get()
                if msg['action_type'] == 'hunt':
                    self.machine.hunt(s=s, q=q, msg=msg)
                elif msg['action_type'] == 'motion':
                    self.machine.motion(s=s, q=q, msg=msg)
                elif msg['action_type'] == 'print':
                    self.machine.print(s=s, q=q, msg=msg)
                self.machine.motion_q.task_done()
            time.sleep(.1)
        logging.debug('THREAD EXIT')
