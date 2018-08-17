"""
Copyright 2017 Scott Wiederhold
This file is part of Glowforge-Utilities.

    Glowforge-Utilities is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Glowforge-Utilities is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Glowforge-Utilities.  If not, see <http://www.gnu.org/licenses/>.


TODO: Error checking/handling of some kind
"""
from . import web_api, _ACTIONS, _STATES
import time
import logging
from ..SETTINGS import settings


"""
Globals used for common values inserted into WSS messages from the device.
"""
# This is added as the ID field. We start at 31 because that is what has
# been observed as normal behaviour from the devices.
response_id = 31

# This field is added as a TIMESTAMP field.
start_time = time.time()


def run_cmd(cmd, **kwargs):
    """
    Runs WS API command
    :param cmd: {str} Command Name
    :param kwargs:
    :return:
    """
    if '_api_' + cmd in globals():
        return globals()['_api_' + cmd](**kwargs)
    else:
        logging.error("UNKNOWN API COMMAND: " + cmd)
        return False


def _api_head_image(s, q, cfg, msg):
    """
    Uploads head image.
    Sends either the laser on or laser off image, selected for the proper thickness.
    :param s: {Session} Requests Session object
    :param q: {Queue} WSS message queue
    :param cfg: {dict} Emulator's configuration dictionary
    :param msg: {dict} WSS Message
    :return:
    """
    logging.info('START')
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id']}, {0: _ACTIONS['head_image'][0], 1: _ACTIONS['head_image'][1]})
    if msg['settings']['HCil'] > 0:
        logging.info('LASER DIODE ON')
        img = 'HEAD_LASER_%s.jpg' % cfg['MATERIAL.THICKNESS']
    else:
        logging.info('LASER DIODE OFF')
        img = 'HEAD_NO_LASER_%s.jpg' % cfg['MATERIAL.THICKNESS']
    web_api.run_cmd('img_upload', s=s, cfg=cfg, img=img, msg=msg)
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id']}, {0: _ACTIONS['head_image'][2]})
    logging.info('COMPLETE')
    return True


def _api_hunt(s, q, cfg, msg):
    """
    Executes hunt actions
    :param s: {Session} Requests Session object
    :param q: {Queue} WSS message queue
    :param cfg: {dict} Emulator's configuration dictionary
    :param msg: {dict} WSS Message
    :return:
    """
    logging.info('START')
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id']}, {0: _ACTIONS['hunt'][0]})
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id']}, {0: _ACTIONS['hunt'][1]})
    # REAL_RUN_TIME will go here
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id']},
                     {0: _ACTIONS['hunt'][2], 1: _ACTIONS['hunt'][3],
                      2: _ACTIONS['hunt'][4]})
    logging.info('COMPLETE')
    return True


def _api_lid_image(s, q, cfg, msg):
    """
    Uploads lid image
    Which image we send depends on whether or not we are homing.  If we are, then we send the homing images
    in the proper sequence.
    :param s: {Session} Requests Session object
    :param q: {Queue} WSS message queue
    :param cfg: {dict} Emulator's configuration dictionary
    :param msg: {dict} WSS Message
    :return:
    """
    logging.info('START')
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id']}, {0: _ACTIONS['lid_image'][0], 1: _ACTIONS['lid_image'][1]})
    if _STATES['homing'] == 0 and _STATES['last_action'] == 'motion':
        # Looks like were are homing again
        _STATES['homing'] = 1
    if _STATES['homing'] != 0:
        logging.info('HOME Step %s' % _STATES['homing'])
        img = 'HOME_%s.jpg' % _STATES['homing']
        web_api.run_cmd('img_upload', s=s, cfg=cfg, img='HOME_%s.jpg' % _STATES['homing'], msg=msg)
        _STATES['homing'] = _STATES['homing'] + 1 if _STATES['homing'] < 4 else 0
    else:
        logging.info('LID IMAGE Selected')
        web_api.run_cmd('img_upload', s=s, cfg=cfg, img='LID_IMAGE.jpg', msg=msg)
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id']}, {0: _ACTIONS['lid_image'][2]})
    logging.info('COMPLETE')
    return True


def _api_motion(s, q, cfg, msg):
    """
    Executes motion commands (not printing)
    :param s: {Session} Requests Session object
    :param q: {Queue} WSS message queue
    :param cfg: {dict} Emulator's configuration dictionary
    :param msg: {dict} WSS Message
    :return:
    """
    logging.info('START')
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id'], 'MOTION_URL': msg['motion_url']}, {0: _ACTIONS['motion'][0]})
    puls = web_api.run_cmd('motion_download', s=s, cfg=cfg, msg=msg)
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id'], 'TOTAL_STEPS': puls.pulse_total}, {0: _ACTIONS['motion'][1]})
    # REAL_RUN_TIME will go here
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id'], 'TOTAL_STEPS': puls.pulse_total},
                     {0: _ACTIONS['motion'][2], 1: _ACTIONS['motion'][3],
                      2: _ACTIONS['motion'][4], 3: _ACTIONS['motion'][5]})
    logging.info('COMPLETE')
    return True


def _api_print(s, q, cfg, msg):
    """
    Executes Print Job
    :param s: {Session} Requests Session object
    :param q: {Queue} WSS message queue
    :param cfg: {dict} Emulator's configuration dictionary
    :param msg: {dict} WSS Message
    :return:
    """
    logging.info('START')
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id'], 'MOTION_URL': msg['motion_url']}, {0: _ACTIONS['print'][0]})
    puls = web_api.run_cmd('motion_download', s=s, cfg=cfg, msg=msg)
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id'], 'TOTAL_STEPS': puls.pulse_total}, {0: _ACTIONS['print'][1]})
    # TODO: REAL_RUN_TIME will go here
    # BREAK HERE TO PAUSE BEFORE BUTTON PUSH
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id'], 'TOTAL_STEPS': puls.pulse_total},
                     {0: _ACTIONS['print'][2], 1: _ACTIONS['print'][3],
                      2: _ACTIONS['print'][4], 3: _ACTIONS['print'][5],
                      4: _ACTIONS['print'][6], 5: _ACTIONS['print'][7],
                      6: _ACTIONS['print'][8], 7: _ACTIONS['print'][9],
                      8: _ACTIONS['print'][10]})
    logging.info('COMPLETE')
    return True


def _api_settings(s, q, cfg, msg):
    """
    Send setting report
    :param s: {Session} Requests Session object
    :param q: {Queue} WSS message queue
    :param cfg: {dict} Emulator's configuration dictionary
    :param msg: {dict} WSS Message
    :return:
    """
    logging.info('START')
    _process_actions(s, q, cfg, {'ACTION_ID': msg['id'],
                                 'SETTINGS': settings.report(cfg)}, {0: _ACTIONS['settings'][0]})
    logging.info('COMPLETE')
    return True


def _process_actions(s, q, cfg, var, actions, **kwargs):
    """
    Processes actions
    :param s: {Session} Requests Session object
    :param q: {Queue} WSS message queue
    :param cfg: {dict} Emulator's configuration dictionary
    :param var: {dict} Values to substitute in the message string
    :param actions: {dict} Actions to process
    :return:
    """
    for group in actions:
        for action in actions[group]:
            if actions[group][action]['act']:
                time.sleep(actions[group][action]['delay'])
                var['ID'] = _rid()
                var['TIMESTAMP'] = _tstamp()
                msg = actions[group][action]['msg']
                if msg != '':
                    var.update(cfg)
                    for item in var:
                        msg = str.replace(msg, '<%s>' % item, str(var[item]))
                if actions[group][action]['api'] == 'web':
                    web_api.run_cmd(actions[group][action]['run'], s=s, cfg=cfg,
                                    action=actions[group][action], **kwargs)
                elif actions[group][action]['api'] == 'ws' and msg != '':
                    q['tx'].put(u'%s\r\n' % msg)
                else:
                    logging.error('UNKNOWN API')
    return True


def _rid():
    """
    Returns ID value to be used in WSS message
    :return:
    """
    global response_id
    response_id += 1
    return response_id


def _tstamp():
    """
    Returns time since start up, adjusted to allow for boot time.
    :return:
    """
    global start_time
    return int(((time.time() - start_time) * 100) + 3800)
