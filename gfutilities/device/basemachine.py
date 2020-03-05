"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from queue import Queue
from requests import Session
from .motion import Motion
from .capture import Capture
from ..service.websocket import send_wss_event


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
        self.motion_q: Queue = Queue()
        self.capture_q: Queue = Queue()
        self.motion_thread: Motion = Motion(self)
        self.capture_thread: Capture = Capture(self)

    def _button_wait(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for "print:waiting" event - waiting for button push
        To be implemented by the child class.
        This is method should return after the big button has been pressed.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def head_image(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Process head image request.
        Sends related start and finish messages, and calls child class handler.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(q, msg, 'head_image:starting')
        self._head_image(s, q, msg)
        send_wss_event(q, msg, 'head_image:completed')

    def _head_image(self, s: Session, q: Queue, msg: dict, settings: dict = None) -> None:
        """
        Child class handler for capturing image from head cam.
        To be implemented by the child class.
        This method should capture the image from the head camera, and upload the resulting image to the Web API.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def hunt(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Home the focus lens.
        Sends related start and finish messages, and calls child class handler.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(q, msg, 'hunt:starting')
        self._hunt(s, q, msg)
        send_wss_event(q, msg, 'hunt:completed')

    def _hunt(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for focus lens homing cycle
        To be implemented by the child class.
        This method should home the lens and set it to the appropriate zeroing offset.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def lid_image(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Process lid image request.
        Sends related start and finish messages, and calls child class handler.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(q, msg, 'lid_image:starting')
        self._lid_image(s, q, msg)
        send_wss_event(q, msg, 'lid_image:completed')

    def _lid_image(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for lid image requests.
        To be implemented by the child class.
        This method should capture the image from the lid camera, and upload the resulting image to the Web API.
       :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def lidar_image(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Process lidar image request.
        Sends related start and finish messages, and calls child class handler to capture
        head images with and without the distance measuring laser enabled.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(q, msg, 'lidar_image:starting')
        self._head_image(s, q, msg, msg['settings'][0])
        self._head_image(s, q, msg, msg['settings'][1])
        send_wss_event(q, msg, 'lidar_image:completed')

    def motion(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Process motion request.
        Sends related start and finish messages, and calls child class handler.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(q, msg, 'motion:starting')
        self._motion(s, q, msg)
        send_wss_event(q, msg, 'motion:completed')

    def _motion(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for motion requests.
        To be implemented by the child class.
        This method should download the specified motion file and execute it.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def print(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Process print request.
        Sends related start and finish messages, and calls child class handlers.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        send_wss_event(q, msg, 'print:starting')
        self._print_download(s, q, msg)
        send_wss_event(q, msg, 'print:download:completed')
        self._button_wait(s, q, msg)
        send_wss_event(q, msg, 'print:warmup:starting')
        self._print_warmup(s, q, msg)
        send_wss_event(q, msg, 'print:running')
        self._print(s, q, msg)
        self._print_return_home(s, q, msg)
        self._print_cooldown(s, q, msg)
        send_wss_event(q, msg, 'print:completed')

    def _print(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for print requests.
        To be implemented by the child class.
        This method executes the print job loaded into the SDMA buffer.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def _print_cooldown(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for print requests.
        To be implemented by the child class.
        This method should spin the fans for period of time after the job has completed.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def _print_download(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for downloading motion files for print operations.
        To be implemented by the child class.
        This method should download the specified motion file and feed it into the SDMA buffer.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def _print_return_home(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for print requests.
        To be implemented by the child class.
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def _print_warmup(self, s: Session, q: Queue, msg: dict) -> None:
        """
        Child class handler for system warmup.
        To be implemented by the child class.
        This method should prepare the system for a print job (i.e. spinning up the fans, etc.)
        :param s: Web API Session
        :type s: Session
        :param q: WSS Transmit Queue
        :type q: Queue
        :param msg: Incoming WSS Message
        :type msg: dict
        :return:
        """
        pass

    def start(self) -> None:
        """
        Start message handling threads.
        :return:
        """
        self.motion_thread.start()
        self.capture_thread.start()

    def stop(self) -> None:
        """
        Stop message handling threads.
        :return:
        """
        self.motion_thread.stop = True
        self.capture_thread.stop = True
        self.motion_thread.join()
        self.capture_thread.join()
