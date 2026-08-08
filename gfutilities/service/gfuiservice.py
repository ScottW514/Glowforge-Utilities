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
from gfutilities.service.dispatch import dispatch_action
from gfutilities.service.websocket import get_session, firmware_check, ws_connect

logger = logging.getLogger(LOGGER_NAME)


class GFUIService:
    """
    Glowforge UI Service Connector
    This connects to the servers specified in the configuration, and interfaces with the service.
    """
    def __init__(self, machine: BaseMachine):
        """
        Class Initialization
        Initialized WSS Queues, and configures logging.
        """
        self.session = None
        self.q_msg_rx = Queue()
        self.q_msg_tx = Queue()
        self.q_capture = Queue()
        self._machine = machine
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
        # Check the factory firmware version the service advertises, and
        # record it for the forgectrl compatibility banner. ForgeFIRM never
        # downloads or installs factory firmware, so the result only informs
        # the operator (see run_update_check / record_factory_latest).
        if get_cfg('FACTORY_FIRMWARE.CHECK'):
            firmware_check(self.session)
        # Establish WebSocket Connection. Pass the session so the client can
        # re-sign-in for a fresh single-use ws_token on every reconnect.
        if not ws_connect(self.q_msg_rx, self.q_msg_tx, self.session):
            return False
        return True

    def run(self) -> None:
        """
        Processes messages from WSS service
        :return:
        """
        self._machine.start(self.session, self.q_msg_tx)
        while True:
            try:
                raw = self.q_msg_rx.get()
            except KeyboardInterrupt:
                break
            try:
                msg = json.loads(raw)
            except (ValueError, TypeError):
                logger.warning('unparseable service message: %r',
                               raw[:200] if isinstance(raw, str) else raw)
                self.q_msg_rx.task_done()
                continue
            logger.info('service action request: %s (%s)',
                        msg.get('action_type'), msg.get('status'))
            result = dispatch_action(self._machine, msg, allow_print=True)
            logger.info('%s (%s) service action %s',
                        msg.get('action_type'), msg.get('status'), result)
            self.q_msg_rx.task_done()
        self._machine.stop()
