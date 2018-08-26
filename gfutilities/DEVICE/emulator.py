"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from . import actions, configuration, connection, websocket, _STATES
from .authentication import authenticate_machine

try:
    import Queue as queue
except ImportError:
    import queue

import json
import time
import logging


class Emulator:
    """
    Glowforge Device Emulator
    This connects to the servers specified in the configuration, and responds the same as the hardware does.
    """
    def __init__(self, cfg_file):
        """
        Class Initialization
        Reads configuration, initialized WSS Queues, and configures logging.
        :param cfg_file: {str} Emulator configuration file
        """
        self.cfg = configuration.parse(cfg_file)
        self.session = None
        self.handlers = {}
        self.q = {'rx': queue.Queue(), 'tx': queue.Queue()}
        # Set up Logging
        if self.cfg['GENERAL.CONSOLE_LOG_LEVEL']:
            logging.basicConfig(format='(%(levelname)s) %(module)s:%(funcName)s %(message)s',
                                level=self._log_level(self.cfg['GENERAL.CONSOLE_LOG_LEVEL']))
        else:
            logging.basicConfig(filename=self.cfg['GENERAL.LOG_FILE'],
                                format='%(asctime)s (%(levelname)s) %(module)s:%(funcName)s %(message)s',
                                level=self._log_level(self.cfg['GENERAL.LOG_LEVEL']))
        logging.info('INITIALIZED')

    def connect(self):
        """
        Authenticates machine to service, checks firmware, and establishes WSS session.
        :return: {bool} Status of connection
        """
        # Grab a persistent web session.  Once authenticated, this session is used for all web API's.
        self.session = connection.get_session(self.cfg)
        # Authenticate machine
        if not authenticate_machine(self.session, self.cfg):
            return False
        # Check for new firmware
        if self.cfg['GENERAL.FIRMWARE_CHECK']:
            fw = actions.run_action('web', 'firmware_check', s=self.session, cfg=self.cfg)
            if fw:
                actions.run_action('web', 'firmware_download', s=self.session, cfg=self.cfg, fw=fw)
        # Establish WebSocket Connection
        if not websocket.ws_connect(self.cfg, self.q):
            return False
        return True

    def run(self):
        """
        Processes messages from WSS service
        :return:
        """
        while True:
            if not self.q['rx'].empty():
                msg = json.loads(self.q['rx'].get())
                logging.info('SERVICE ACTION: %s (%s)' % (msg['action_type'], msg['status']))
                if msg['status'] == 'ready':
                    actions.run_action('ws', msg['action_type'],
                                       s=self.session, q=self.q, cfg=self.cfg, msg=msg, handlers=self.handlers)
                    logging.info('%s (%s) SERVICE ACTION PROCESSED' % (msg['action_type'], msg['status']))
                    _STATES['last_action'] = msg['action_type']
                else:
                    logging.info('%s (%s) SERVICE ACTION IGNORED' % (msg['action_type'], msg['status']))
                self.q['rx'].task_done()
            time.sleep(.5)

    def set_handler(self, name, handler):
        """
        Sets method to handle print calls.
        :param name: {str} Name of Handler
        :param handler: {object} Print Handler Method
        :return:
        """
        self.handlers[name] = handler

    def _log_level(self, level_str):
        """
        Returns logging log level object based on provided string.
        :param level_str: {str} Desired logging level
        :return: {logging.level} Logging level object
        """
        levels = {
            'CRITICAL': logging.CRITICAL, 'ERROR': logging.ERROR, 'WARNING': logging.WARNING, 'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }
        if level_str in levels:
            return levels[level_str]
        else:
            return logging.INFO
