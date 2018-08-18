"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from .connection import request, download_file
from ..MOTION import motion
from . import _ACTIONS
import time
import logging
import json


def run_cmd(cmd, **kwargs):
    """
    Runs WEB API command
    :param cmd: {str} Command Name
    :param kwargs:
    :return:
    """
    if '_api_' + cmd in globals():
        return globals()['_api_' + cmd](**kwargs)
    else:
        logging.error("UNKNOWN API COMMAND: " + cmd)
        return False


def message(cmd, **kwargs):
    """
    Runs WEB Message command
    :param cmd: {str} Message Command Name
    :param kwargs:
    :return:
    """
    if '_api_msg_' + cmd in globals():
        return globals()['_api_msg_' + cmd](**kwargs)
    else:
        logging.error("UNKNOWN API MSG COMMAND: " + cmd)
        return False


def _api_firmware_check(s, cfg):
    """
    Checks for the latest version of available firmware.
    :param s: {Session} Requests Session object
    :param cfg: {dict} Emulator's configuration dictionary
    :return: {bool|dict} Returns False if configured firmware is equal latest.
    Returns a {dict} if new firmware is available.
    {'version': '<new version>', 'download_url': '<url to download firmware>'}
    """
    logging.info('CHECKING')
    _process_actions(s, cfg, {'MILLI_EPOCH': _milli_epoch()}, {0: _ACTIONS['firmware_check'][0]})
    r = request(s, cfg['SERVICE.SERVER_URL'] + '/update/current', 'GET')
    if not r:
        logging.error('FAILED')
        return False
    rj = r.json()
    logging.debug(rj)
    _process_actions(s, cfg, {'AVAILABLE_FIRMWARE': rj['version']},
                    {0: _ACTIONS['firmware_check'][1], 1: _ACTIONS['firmware_check'][2]})
    if not rj['version'] == cfg['MACHINE.FIRMWARE']:
        logging.info('New Firmware Available: Installed (%s), Available (%s)'
                     % (cfg['MACHINE.FIRMWARE'], rj['version']))
        return rj
    else:
        logging.info('LATEST ALREADY INSTALLED.')
        return False


def _api_firmware_download(s, cfg, fw):
    """
    Downloads latest firmware to directory set in config.
    :param s: {Session} Requests Session object
    :param cfg: {dict} Emulator's configuration dictionary
    :param fw: {dict} Dictionary returned by _api_firmware_check()
    :return: {bool} True
    """
    logging.info('DOWNLOADING')
    download_file(s, fw['download_url'], '%s/glowforge-fw-v%s.fw' % (cfg['GENERAL.FIRMWARE_DIR'], fw['version']))
    logging.info('COMPLETE.')
    return True


def _api_img_upload(s, cfg, img, msg):
    """
    Uploads head/lid image
    :param s: {Session} Requests Session object
    :param cfg: {dict} Emulator's configuration dictionary
    :param img: {dict} Dictionary returned by _api_firmware_check()
    :param msg: {dict} WSS message
    :return:
    """
    logging.info('START')
    img = open('%s/%s' % (cfg['GENERAL.IMAGE_DIR'], img), 'rb')
    url = cfg['SERVICE.SERVER_URL'] + '/api/machines/%s/%s' % (msg['action_type'], msg['id'])
    headers = {'Content-Type': 'image/jpeg'}
    r = request(s, url, 'POST', data=img.read(), headers=headers)
    logging.debug(r.json)
    if not r:
        return False
    logging.info('COMPLETE')
    return True


def _api_motion_download(s, cfg, msg):
    """
    Downloads Motion file
    :param s: {Session} Requests Session object
    :param msg: {dict} WSS message
    :return: {Motion} Motion file object
    """
    logging.info('DOWNLOADING')
    file_name = '%s/%s_%s.puls' % (cfg['GENERAL.MOTION_DIR'], time.strftime("%Y-%m-%d_%H%M%S"), msg['action_type'])
    download_file(s, msg['motion_url'], file_name)
    logging.info('COMPLETE')
    return motion.Motion(file_name)


def _api_status(s, **kwargs):
    """
    Submits status update to status API
    :param s: {Session} Requests Session object
    :param cfg: {dict} Emulator's configuration dictionary
    :return:
    """
    cfg = kwargs['cfg']
    logging.info('STARTING')
    r = request(s, cfg['SERVICE.SERVER_URL'] + '/api/machines/status',
                'PUT', data=json.dumps({'firmware': {'version': cfg['MACHINE.FIRMWARE'],
                                                     'scm': cfg['MACHINE.APP_VERSION']},
                                        'local_ip_address': cfg['MACHINE.IP_ADDRESS']}),
                headers={'Content-Type': 'application/json'})
    if not r:
        return False
    logging.debug(r.json)
    logging.info('SUCCESS')
    return True


def _api_msg_event(s, cfg, msg):
    """
    Sends EVENT to event API
    :param s: {Session} Requests Session object
    :param cfg: {dict} Emulator's configuration dictionary
    :param msg: {str} Event message
    :return:
    """
    logging.info('START')
    logging.debug(msg)
    r = request(s, cfg['SERVICE.STATUS_SERVICE_URL'] + '/api/event', 'POST', data=msg)
    if not r.status_code == 200:
        logging.error('FAILED: ' + r.reason)
        return False
    else:
        return True


def _process_actions(s, cfg, var, actions):
    """
    Processes actions
    :param s: {Session} Requests Session object
    :param cfg: {dict} Emulator's configuration dictionary
    :param var: {dict} Values to substitute in the message string
    :param actions: {dict} Actions to process
    :return:
    """
    for group in actions:
        for action in actions[group]:
            if actions[group][action]['act']:
                time.sleep(actions[group][action]['delay'])
                msg = actions[group][action]['msg']
                if msg != '':
                    var.update(cfg)
                    for item in var:
                        msg = str.replace(msg, '<%s>' % item, str(var[item]))
                message(actions[group][action]['run'], msg=msg, s=s, cfg=cfg)
    return True


def _milli_epoch():
    """
    Returns Unix epoch in milliseconds
    :return:
    """
    return int(time.time() * 1000)
