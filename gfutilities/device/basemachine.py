"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import logging
from queue import Queue
from requests import Session
from threading import Thread
from typing import Union

from gfutilities._common import *
from gfutilities.configuration import set_cfg
from gfutilities.device.settings import send_report, get_machine_setting
from gfutilities.service.websocket import send_wss_event

logger = logging.getLogger(LOGGER_NAME)


class BaseMachine:
    """
    BaseMachine Base Class
    Serves as the foundation for emulator and machine control classes.
    Implements the basic functions required for operation with the Glowforge online service.
    """
    def __init__(self):
        """
        Initializes the object, child threads and message queues.
        """
        self._action_thread: _ActionThread = _ActionThread(self, {})
        self._q_msg_tx: Union[Queue, None] = None
        self.running_action_id: Union[int, None] = 0
        self.running_action_type: Union[str, None] = None
        self._running_action_cancelled: bool = False
        self._session: Session = Union[Queue, None]

        set_cfg('FACTORY_FIRMWARE.FW_VERSION', get_machine_setting('MCov'), True)
        set_cfg('FACTORY_FIRMWARE.APP_VERSION', get_machine_setting('MCdv'), True)

    def _ok_to_run_action(self, action_id: str, msg_type: str, status: str) -> bool:
        """
        Checks the action against any current running actions.
        If this a request to cancel an action:
            - If the action is currently running, it sets the _running_action_cancelled flag as True
            - If the action is not currently running, it sends a cancelled message to the service.
            - For both conditions, it returns False
        If there are not any currently running actions, it sets this as the current running action and returns True.
        If there is a current running action, and this is not a request to cancel it, sends a cancelled message
        to the service for this requested action, and returns false.
        :param action_id: Action ID
        :type action_id: str
        :param msg_type: Action Type
        :type msg_type: str
        :param status: Status of message (either 'ready' or 'cancelled')
        :type status: str
        :return: Return True if this it is ok to run this action, False if not
        :rtype: bool
        """
        action_id = int(action_id)
        if action_id == self.running_action_id and status == 'cancelled':
            logger.debug('action %s (%s) cancellation received' % (action_id, msg_type))
            self._running_action_cancelled = True
            return False
        elif self.running_action_id or status == 'cancelled':
            return False
        else:
            logger.debug('running action set to %s (%s)' % (action_id, msg_type))
            self.running_action_id = action_id
            self.running_action_type = msg_type
            self._running_action_cancelled = False
            return True

    def _button_wait(self, msg: dict) -> None:
        """
        Child class handler for "print:waiting" event - waiting for button push
        To be implemented by the child class.
        This is method should return after the big button has been pressed.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        raise NotImplementedError

    def head_image(self, msg: dict) -> None:
        """
        Process head image request.
        Sends related start and finish messages, and calls child class handler.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(self._q_msg_tx, msg['id'], 'head_image:starting')
        self._head_image(msg)
        send_wss_event(self._q_msg_tx, msg['id'], 'head_image:completed')

    def _head_image(self, msg: dict, settings: dict = None) -> None:
        """
        Child class handler for capturing image from head cam.
        To be implemented by the child class.
        This method should capture the image from the head camera, and upload the resulting image to the Web API.
        :param msg: Incoming WSS Message
        :type msg: dict
        :param settings: Camera settings
        :type settings: dict
        :return:
        """
        raise NotImplementedError

    def hunt(self, msg: dict) -> None:
        """
        Home the focus lens.
        Sends related start and finish messages, and calls child class handler.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(self._q_msg_tx, msg['id'], 'hunt:starting')
        self._hunt(msg)
        send_wss_event(self._q_msg_tx, msg['id'], 'hunt:completed')

    def _hunt(self, msg: dict) -> None:
        """
        Child class handler for focus lens homing cycle
        To be implemented by the child class.
        This method should home the lens and set it to the appropriate zeroing offset.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        raise NotImplementedError

    def _initialize(self) -> None:
        """
        Child class handler for initializing the machine
        To be implemented by the child class.
        :return:
        """
        raise NotImplementedError

    def lid_image(self, msg: dict) -> None:
        """
        Process lid image request.
        Sends related start and finish messages, and calls child class handler.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(self._q_msg_tx, msg['id'], 'lid_image:starting')
        self._lid_image(msg)
        send_wss_event(self._q_msg_tx, msg['id'], 'lid_image:completed')

    def _lid_image(self, msg: dict) -> None:
        """
        Child class handler for lid image requests.
        To be implemented by the child class.
        This method should capture the image from the lid camera, and upload the resulting image to the Web API.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        raise NotImplementedError

    def lidar_image(self, msg: dict) -> None:
        """
        Process lidar image request.
        Sends related start and finish messages, and calls child class handler to capture
        head images with and without the distance measuring laser enabled.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(self._q_msg_tx, msg['id'], 'lidar_image:starting')
        self._head_image(msg, msg['settings'][0])
        send_wss_event(self._q_msg_tx, msg['id'], 'lidar_image:completed')

    def motion(self, msg: dict) -> None:
        """
        Process motion request.
        Sends related start and finish messages, and calls child class handler.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(self._q_msg_tx, msg['id'], msg['action_type'] + ':starting')
        self._motion(msg)
        if self._running_action_cancelled:
            self._send_cancelled_message(msg['id'], msg['action_type'])
        else:
            send_wss_event(self._q_msg_tx, msg['id'], msg['action_type'] + ':completed')

    def _motion(self, msg: dict) -> None:
        """
        Child class handler for motion requests.
        To be implemented by the child class.
        This method should download the specified motion file and execute it.
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        raise NotImplementedError

    def run_capture(self, msg: dict) -> None:
        """
        Process capture request.
        Fires up CaptureThread thread to handle image request.
        Interface for GFUI Service
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        if self._ok_to_run_action(msg['id'], msg['action_type'], msg['status']):
            if not self._action_thread.is_alive():
                self._action_thread = _ActionThread(self, msg)
                self._action_thread.start()

    def run_puls(self, msg: dict) -> None:
        """
        Process pulse file.
        Fires up MotionThread thread to handle puls file request.
        Interface for GFUI Service
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        if self._ok_to_run_action(msg['id'], msg['action_type'], msg['status']):
            if not self._action_thread.is_alive():
                self._action_thread = _ActionThread(self, msg)
                self._action_thread.start()

    def run_settings_report(self, msg: dict) -> None:
        """
        Send settings report.
        Interface for GFUI Service
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        if self._ok_to_run_action(msg['id'], msg['action_type'], msg['status']):
            send_report(self._q_msg_tx, msg)
        self.running_action_id = None

    def _shutdown(self) -> None:
        """
        Child class handler for shutting down the machine
        To be implemented by the child class.
        :return:
        """
        raise NotImplementedError

    def _send_cancelled_message(self, action_id: int, action_type: str):
        send_wss_event(self._q_msg_tx, action_id, '%s:cancelled' % action_type)

    def start(self, session: Session, msq_tx_q: Queue) -> None:
        """
        Initialize Machine and Start message handling threads.
        :param session: WSS Session
        :type session: Session
        :param msq_tx_q: WSS Msg Tx Queue
        :type msq_tx_q: Queue
        :return:
        """
        logger.debug('starting')
        self._session = session
        self._q_msg_tx = msq_tx_q
        self._initialize()
        logger.debug('started')

    def stop(self) -> None:
        """
        Stop message handling threads.
        :return:
        """
        logger.debug('stopping')
        self._shutdown()
        logger.debug('stopped')


class _ActionThread(Thread):
    """
    ActionThread
    Responds to incoming WSS events to run an action
    """
    def __init__(self, machine: BaseMachine, msg: dict):
        """
        Initialize ActionThread Dispatcher
        :param machine: Machine object
        :type machine: BaseMachine
        :param msg: Incoming WSS Message
        :type msg: dict
        """
        self._machine = machine
        self._msg = msg
        Thread.__init__(self)

    def run(self) -> None:
        logger.debug('action thread start')
        if self._msg['action_type'] == 'lid_image':
            self._machine.lid_image(self._msg)
        elif self._msg['action_type'] == 'head_image':
            self._machine.head_image(self._msg)
        elif self._msg['action_type'] == 'lidar_image':
            self._machine.lidar_image(self._msg)
        elif self._msg['action_type'] == 'hunt':
            self._machine.hunt(self._msg)
        elif self._msg['action_type'] in ['motion', 'print']:
            self._machine.motion(self._msg)
        self._machine.running_action_id = None
        self._machine.running_action_type = None
        logger.debug('action thread stop')


__all__ = ['BaseMachine']
