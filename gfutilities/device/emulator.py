"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import logging
import time
from requests import Session
from queue import Queue
from .basemachine import BaseMachine
from ..puls import PulseData
from ..configuration import get_cfg
from ..service.websocket import download_file, img_upload


class Emulator(BaseMachine):
    """
    Glowforge Device Emulator
    This connects to the servers specified in the configuration, and responds the same as the hardware does.
    """
    def __init__(self):
        """
        Initialize object
        """
        BaseMachine.__init__(self)
        # Track which step in the homing process we are at.
        # Example script has 5 saved head images, which are uploaded to the service in sequence to
        # emulate the homing process.  Files are located in _RESOURCES/IMG
        # HOME_1.jpg: Image of the head located at expected center position
        #             This image was taken with the head already in the calibrated position to speed up the process.
        # HOME_2.jpg: Image after first retreat move
        # HOME_3.jpg: Image after second retreat move
        # HOME_4.jpg: Image after third retreat move
        # LID_IMAGE.jpg: Image of bed with Proofgrade(tm) material
        #                This image is sent for every none-homing lid_image request
        self._homing_stage = 0 if get_cfg('MACHINE.BYPASS_HOMING') else 1
        # Used to track the action just before a lid_image request. This is used to detect homing operations after
        # the initial start up (after a print job, for instance)
        self._last_action = None

    def _button_wait(self, s: Session, q: Queue, msg: dict) -> None:
        pass

    def _head_image(self, s: Session, q: Queue, msg: dict, settings: dict = None) -> None:
        if settings is not None and settings.get('HCil') > 0:
            img = 'HEAD_LASER_%s.jpg' % get_cfg('MATERIAL.THICKNESS')
        else:
            img = 'HEAD_NO_LASER_%s.jpg' % get_cfg('MATERIAL.THICKNESS')
        with open('%s/%s' % (get_cfg('GENERAL.IMAGE_DIR'), img), 'rb') as f:
            img_upload(s, f.read(), msg)
        self._last_action = 'head_image'

    def _hunt(self, s: Session, q: Queue, msg: dict) -> None:
        self._last_action = 'hunt'
        self._motion_download(s, msg)

    def _lid_image(self, s: Session, q: Queue, msg: dict) -> None:
        if self._homing_stage == 0 and self._last_action == 'motion':
            # Looks like were are homing again
            self._homing_stage = 1
        if self._homing_stage != 0:
            logging.info('HOME Step %s' % self._homing_stage)
            img = 'HOME_%s.jpg' % self._homing_stage
            self._homing_stage = self._homing_stage + 1 if self._homing_stage < 4 else 0
        else:
            img = 'LID_IMAGE.jpg'
        with open('%s/%s' % (get_cfg('GENERAL.IMAGE_DIR'), img), 'rb') as f:
            img_upload(s, f.read(), msg)
        self._last_action = 'lid_image'

    def _motion(self, s: Session, q: Queue, msg: dict) -> None:
        self._motion_download(s, msg)
        self._last_action = 'motion'

    def _motion_download(self, s: Session, msg: dict) -> PulseData:
        logging.info('DOWNLOADING')
        file_name = '%s/%s_%s.puls' % (get_cfg('GENERAL.MOTION_DIR'),
                                       time.strftime("%Y-%m-%d_%H%M%S"), msg['action_type'])
        download_file(s, msg['motion_url'], file_name)
        logging.info('COMPLETE')
        return PulseData(file_name)

    def _print(self, s: Session, q: Queue, msg: dict) -> None:
        self._last_action = 'print'
        pass

    def _print_cooldown(self, s: Session, q: Queue, msg: dict) -> None:
        pass

    def _print_download(self, s: Session, q: Queue, msg: dict) -> None:
        self._motion_download(s, msg)

    def _print_return_home(self, s: Session, q: Queue, msg: dict) -> None:
        pass

    def _print_warmup(self, s: Session, q: Queue, msg: dict) -> None:
        pass
