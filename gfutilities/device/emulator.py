"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import json
import logging
import time

from gfutilities._common import *
from gfutilities.configuration import get_cfg
from gfutilities.device.basemachine import BaseMachine
from gfutilities.service.websocket import load_motion, img_upload, send_wss_event

logger = logging.getLogger(LOGGER_NAME)


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
        self._homing_stage = 0 if get_cfg('EMULATOR.BYPASS_HOMING') else 1
        # Used to track the action just before a lid_image request. This is used to detect homing operations after
        # the initial start up (after a print job, for instance)
        self._last_action = None

    def _button_wait(self, msg: dict) -> None:
        pass

    def _head_image(self, msg: dict, settings: dict = None) -> None:
        if settings is not None and settings.get('HCil') > 0:
            img = 'HEAD_LASER_%s.jpg' % get_cfg('EMULATOR.MATERIAL_THICKNESS')
        else:
            img = 'HEAD_NO_LASER_%s.jpg' % get_cfg('EMULATOR.MATERIAL_THICKNESS')
        with open('%s/%s' % (get_cfg('EMULATOR.IMAGE_SRC_DIR'), img), 'rb') as f:
            img_upload(self._session, f.read(), msg)
        self._last_action = 'head_image'

    def _hunt(self, msg: dict) -> None:
        self._last_action = 'hunt'
        self._motion_download(msg)

    def _initialize(self) -> None:
        pass

    def _lid_image(self, msg: dict) -> None:
        if self._homing_stage == 0 and self._last_action == 'motion':
            # Looks like were are homing again
            self._homing_stage = 1
        if self._homing_stage != 0:
            logger.info('HOME Step %s' % self._homing_stage)
            img = 'HOME_%s.jpg' % self._homing_stage
            self._homing_stage = self._homing_stage + 1 if self._homing_stage < 4 else 0
        else:
            img = 'LID_IMAGE.jpg'
        with open('%s/%s' % (get_cfg('EMULATOR.IMAGE_SRC_DIR'), img), 'rb') as f:
            img_upload(self._session, f.read(), msg)
        self._last_action = 'lid_image'

    def _motion(self, msg: dict) -> None:
        # Download puls file from service
        self._motion_download(msg)
        if msg['action_type'] == 'print':
            send_wss_event(self._q_msg_tx, msg['id'], 'print:download:completed')
            self._button_wait(msg)
            if not self._running_action_cancelled:
                send_wss_event(self._q_msg_tx, msg['id'], 'print:warmup:starting')
        # Run motion job
        if not self._running_action_cancelled:
            if msg['action_type'] == 'print':
                send_wss_event(self._q_msg_tx, msg['id'], 'print:running')

        self._last_action = msg['action_type']

    def _motion_download(self, msg: dict):
        logger.info('DOWNLOADING')
        base_file_name = '%s/%s_%s' % (get_cfg('EMULATOR.MOTION_DL_DIR'),
                                       time.strftime("%Y-%m-%d_%H%M%S"), msg['action_type'])
        info = load_motion(self._session, msg['motion_url'], base_file_name + '.puls')
        with open(base_file_name + '.info', 'w') as f:
            f.write(json.dumps(info, sort_keys=True, indent=4, default=str) + '\n')
        logger.debug('Header: %s' % info)
        logger.info('COMPLETE')
        return

    def _shutdown(self) -> None:
        pass
