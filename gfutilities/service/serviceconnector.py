"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import json
import time
import logging
from queue import Queue
from typing import Union
from ..configuration import get_cfg, parse
from ..service.websocket import get_session, firmware_check, firmware_download, ws_connect
from ..service.authentication import authenticate_machine
from ..device.basemachine import BaseMachine
from ..device.settings import send_report


class ServiceConnector:
    """
    Glowforge Service Connector
    This connects to the servers specified in the configuration, and interfaces with the service.
    """
    def __init__(self, cfg_path: str, machine: BaseMachine):
        """
        Class Initialization
        Initialized WSS Queues, and configures logging.
        :param cfg_path: Path to configuration file
        :type cfg_path: str
        """
        parse(cfg_path)
        self.session = None
        self.machine = machine
        self.q_rx = Queue()
        self.q_tx = Queue()
        self.q_capture = Queue()

        # Set up Logging
        if get_cfg('GENERAL.CONSOLE_LOG_LEVEL'):
            logging.basicConfig(format='(%(levelname)s) %(module)s:%(funcName)s %(message)s',
                                level=self._log_level(get_cfg('GENERAL.CONSOLE_LOG_LEVEL')))
        else:
            logging.basicConfig(filename=get_cfg('GENERAL.LOG_FILE'),
                                format='%(asctime)s (%(levelname)s) %(module)s:%(funcName)s %(message)s',
                                level=self._log_level(get_cfg('GENERAL.LOG_LEVEL')))
        logging.info('INITIALIZED')

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
        if get_cfg('GENERAL.FIRMWARE_CHECK'):
            fw = firmware_check(self.session)
            if fw:
                firmware_download(self.session, fw)
        # Establish WebSocket Connection
        if not ws_connect(self.q_rx, self.q_tx):
            return False
        return True

    def run(self) -> None:
        """
        Processes messages from WSS service
        :return:
        """
        self.machine.start()
        while True:
            try:
                if not self.q_rx.empty():
                    msg = json.loads(self.q_rx.get())
                    logging.info('SERVICE ACTION: %s (%s)' % (msg['action_type'], msg['status']))
                    if msg['status'] == 'ready':
                        if msg['action_type'] == 'settings':
                            send_report(self.q_tx, msg)
                        elif 'image' in msg['action_type']:
                            self.machine.capture_q.put((self.session, self.q_tx, msg))
                        elif msg['action_type'] in ('hunt', 'motion', 'print'):
                            self.machine.motion_q.put((self.session, self.q_tx, msg))
                        logging.info('%s (%s) SERVICE ACTION PROCESSED' % (msg['action_type'], msg['status']))
                    else:
                        logging.info('%s (%s) SERVICE ACTION IGNORED' % (msg['action_type'], msg['status']))
                    self.q_rx.task_done()
                time.sleep(.1)
            except KeyboardInterrupt:
                break
        self.machine.stop()

    @staticmethod
    def _log_level(level_str: str) -> \
            Union[logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]:
        """
        Returns logging log level object based on provided string.
        :param level_str: Desired logging level
        :type level_str: str
        :return: Logging level object
        :rtype: Union[logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
        """
        levels = {
            'CRITICAL': logging.CRITICAL, 'ERROR': logging.ERROR, 'WARNING': logging.WARNING, 'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }
        if level_str in levels:
            return levels[level_str]
        else:
            return logging.INFO
