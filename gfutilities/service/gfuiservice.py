"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import logging
import json
from queue import Queue

from gfutilities._common import *
from gfutilities.configuration import *
from gfutilities.device.basemachine import BaseMachine
from gfutilities.service.authentication import authenticate_machine
from gfutilities.service.websocket import get_session, firmware_check, firmware_download, ws_connect

logger = logging.getLogger(LOGGER_NAME)


class GFUIService:
    """
    Glowforge UI Service Connector
    This connects to the servers specified in the configuration, and interfaces with the service.
    """
    def __init__(self):
        """
        Class Initialization
        Initialized WSS Queues, and configures logging.
        """
        self.session = None
        self.q_msg_rx = Queue()
        self.q_msg_tx = Queue()
        self.q_capture = Queue()
        logger.info('INITIALIZED')

    def connect(self) -> bool:
        """
        Authenticates machine to service, checks firmware, and establishes WSS session.
        :return: Status of connection
        :rtype: bool
        """
        # Grab a persistent web session.  Once authenticated, this session is used for all web API's.
        self.session = get_session()
        # Authenticate machine
        if not authenticate_machine(self.session):
            return False
        # Check for new firmware
        if get_cfg('FACTORY_FIRMWARE.CHECK'):
            fw = firmware_check(self.session)
            if fw:
                firmware_download(self.session, fw)
        # Establish WebSocket Connection
        if not ws_connect(self.q_msg_rx, self.q_msg_tx):
            return False
        return True

    def run(self, machine: BaseMachine) -> None:
        """
        Processes messages from WSS service
        :return:
        """
        machine.start(self.session, self.q_msg_tx)
        while True:
            try:
                msg = json.loads(self.q_msg_rx.get())
                logger.info('service action request: %s (%s)' % (msg['action_type'], msg['status']))
                result = 'dispatched'
                if msg['action_type'] == 'settings' and msg['status'] == 'ready':
                    machine.run_settings_report(msg)
                elif 'image' in msg['action_type']:
                    machine.run_capture(msg)
                elif msg['action_type'] in ('hunt', 'motion', 'print'):
                    machine.run_puls(msg)
                else:
                    result = 'ignored'
                logger.info('%s (%s) service action %s' % (msg['action_type'], msg['status'], result))
                self.q_msg_rx.task_done()
            except KeyboardInterrupt:
                break
        machine.stop()
