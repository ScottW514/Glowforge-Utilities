"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from datetime import timedelta
import json
import logging
from pathlib import Path
from queue import Queue
from requests import Request, Response, Session
from threading import Thread
import time
from typing import Union

from lomond import WebSocket
from lomond.persist import persist

from gfutilities._common import *
from gfutilities.configuration import get_cfg, set_cfg
from gfutilities.puls import decode_all_steps

start_time = time.time()
response_id = 31

logger = logging.getLogger(LOGGER_NAME)


class WsClient(Thread):
    """
    Web Socket Client
    Establishes a persistent WSS client that launches a separate thread to handle WSS operations.
    Spools incoming messages to the q_msg_rx Queue, and sends any messages placed into the q_msg_tx Queue.
    """
    def __init__(self, q_rx: Queue, q_tx: Queue):
        """
        Class Initializer
        :param q_rx: WSS RX Message Queue
        :type q_rx: Queue
        :param q_tx: WSS TX Message Queue
        :type q_tx: Queue
        """
        self.msg_q_rx = q_rx
        self.msg_q_tx = q_tx
        self.stop = False
        self.ready = False
        self.ws = WebSocket(url=get_cfg('SERVICE.STATUS_SERVICE_URL') + '/' + get_cfg('SESSION.WS_TOKEN'),
                            protocols=['glowforge'], agent=get_cfg('SESSION.USER_AGENT'))
        self.ignore_events = ['ping', 'pong', 'poll', 'connecting', 'connected']
        Thread.__init__(self)

    def run(self) -> None:
        """
        Thread loop
        Listens for WS messages, and adds them the q_msg_rx Queue.
        Monitors the q_msg_tx, and sends any messages it finds.
        Handles PING, PONG, and POLL messages.
        :return:
        """
        for event in persist(self.ws):
            if event.name not in self.ignore_events:
                logger.info('RX-EVENT: ' + event.name)
                logger.debug(event)
            if self.stop:
                logger.info('STOP REQUESTED')
                break
            # WS reporting session is established
            if event.name == 'ready':
                self.ready = True
            # Service has sent us a text message
            elif event.name == 'text':
                logger.debug(event.text)
                self.msg_q_rx.put(event.text)
            elif event.name not in self.ignore_events:
                logger.error('UNKNOWN RX-EVENT: ' + event.name)
            while self.ready:
                if not self.msg_q_tx.empty():
                    send_msg = self.msg_q_tx.get()
                    logger.info('TX-EVENT: ' + send_msg.strip())
                    self.ws.send_text(send_msg)
                    self.msg_q_tx.task_done()
                else:
                    break
        logger.info('CLOSING')
        self.ws.close()


def _byte_to_int(data: bytes) -> int:
    """
    Returns integer value of big endian byte data
    :param data:
    :return: Integer value
    :rtype: int
    """
    return ord(data[0:1]) + (ord(data[1:2]) * 0x100) + (ord(data[2:3]) * 0x10000) + (ord(data[3:4]) * 0x1000000)


def firmware_check(s: Session) -> Union[dict, bool]:
    """
    Checks for the latest version of available firmware.
    Returns a {dict} if new firmware is available.
    {'version': '<new version>', 'download_url': '<url to download firmware>'}
    :param s: Requests Session object
    :type s: Session
    :return: Returns False if configured firmware is equal latest.
    :rtype: Union[dict, bool]
    """
    logger.info('CHECKING')
    r = request(s, get_cfg('SERVICE.SERVER_URL') + '/update/current', 'GET')
    if not r:
        logger.error('FAILED')
        return False
    rj = r.json()
    logger.debug(rj)
    if rj['version'] is not None and not rj['version'] == get_cfg('FACTORY_FIRMWARE.FW_VERSION'):
        logger.info('New Firmware Available: Installed (%s), Available (%s)'
                    % (get_cfg('FACTORY_FIRMWARE.FW_VERSION'), rj['version']))
        return rj
    else:
        logger.info('LATEST ALREADY INSTALLED.')
        return False


def firmware_download(s: Session, fw: dict) -> bool:
    """
    Downloads latest firmware to directory set in config.
    :param s: Requests Session object
    :type s: Session
    :param fw: Dictionary returned by _api_firmware_check()
    :type fw: dict
    :return: {bool} True
    :rtype: bool
    """
    logger.info('DOWNLOADING')
    Path(get_cfg('FACTORY_FIRMWARE.DOWNLOAD_DIR')).mkdir(parents=True, exist_ok=True)
    r = request(s, fw['download_url'], 'GET', stream=True)

    with open('%s/glowforge-fw-v%s.fw' % (get_cfg('FACTORY_FIRMWARE.DOWNLOAD_DIR'), fw['version']), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    logger.info('COMPLETE.')
    return True


def get_session() -> Session:
    """
    Creates web api session object.
    :return: Requests Session object
    :rtype: Session
    """
    s = Session()
    set_cfg('SESSION.USER_AGENT', 'OpenGlow/%s' % get_cfg('FACTORY_FIRMWARE.FW_VERSION'))
    s.headers.update({'user-agent': get_cfg('SESSION.USER_AGENT')})
    logger.debug('Returning object : %s' % s)
    return s


def img_upload(s: Session, img: bytes, msg: dict) -> bool:
    """
    Uploads head/lid image
    :param s: Requests Session object
    :type s: Session
    :param img: Path to file to upload, or bytes object containing image
    :type img: bytes
    :param msg: WSS message
    :type msg: dict
    :return:
    :rtype: bool
    """
    logger.info('START')
    url = get_cfg('SERVICE.SERVER_URL') + '/api/machines/%s/%s' % (msg['action_type'], msg['id'])
    headers = {'Content-Type': 'image/jpeg'}
    r = request(s, url, 'POST', data=img, headers=headers)
    if not r:
        logger.debug(r)
        return False
    else:
        logger.debug(r.json)
    logger.info('COMPLETE')
    return True


def load_motion(s: Session, url: str, out_file: str) -> Union[dict, bool]:
    """
    Downloads motion/print file, parses header
    :param s: Requests Session object
    :type s: Session
    :param url: Target URL
    :type url: str
    :param out_file: Where to write the results
    :type out_file: str
    :return: Header dict or False on failure
    :rtype: Union[dict, bool]
    """
    r = request(s, url, 'GET', stream=True)
    info = {
        'header_data': {},
        'header_len': 0,
        'size': 0,
        'run_time': None,
    }
    with open(out_file, 'wb') as f:
        res = r.iter_content(chunk_size=1024)
        puls_data = next(res)
        if puls_data[1:4].decode() != 'GF1':
            logger.error('received data not a GF puls file')
            return False
        info['header_len'] = _byte_to_int(puls_data[4:8]) - 8
        s = 8
        while s < (info['header_len'] + 8):
            info['header_data'][puls_data[s:s + 4].decode()] = _byte_to_int(puls_data[s + 4:s + 8])
            s += 8
        size = len(puls_data[s:])
        stat = decode_all_steps(puls_data[s:])
        # TODO: REMOVE THIS TEMP RAW WRITE - ONLY FOR QUICK TESTING
        base_file_name = '%s/%s' % (str(Path(get_cfg('LOGGING.FILE')).parent), time.strftime("%Y-%m-%d_%H%M%S"))
        raw = open(base_file_name + '.puls', 'wb')
        raw.write(puls_data)
        f.write(puls_data[s:])
        for chunk in res:
            if chunk:
                size = size + len(chunk)
                stat = decode_all_steps(chunk, stat)
                f.write(chunk)
                raw.write(chunk)
        raw.close()
        info['size'] = size
        info['run_time'] = timedelta(seconds=size / info['header_data']['STfr'])
        info['stats'] = stat
        raw = open(base_file_name + '.info', 'w')
        raw.write(json.dumps(info, sort_keys=True, indent=4, default=str) + '\n')
        raw.close()
        return info


def request(s: Session, url: str, method: str, timeout: int = 15, stream: bool = False, **kwargs) \
        -> Union[Response, bool]:
    """
    Submits requests to provided url using the established Session object
    :param s: Requests Session object
    :type s: Session
    :param url: Target URL
    :type url: str
    :param method: Method for the request
    :type method: str
    :param timeout: Timeout
    :type timeout: int
    :param stream: Stream
    :type stream: bool
    :param kwargs:
    :return: Requests Response object, or False on error.
    :rtype: Union[Response, bool]
    """
    req = Request(method, str.replace(str(url), 'wss://', 'https://'), **kwargs)
    req = s.prepare_request(req)
    r = s.send(req, stream=stream, timeout=timeout)
    if r.status_code != 200:
        logger.error('FAILED: ' + r.reason)
        return False
    else:
        return r


def send_wss_event(msg_q_tx: Queue, action_id: Union[int, None], event: str, **kwargs):
    global response_id
    global start_time
    response_id += 1

    if 'data' in kwargs:
        data = ',"%s":%s' % (kwargs['data']['key'], kwargs['data']['value'])
    else:
        data = ''
    if action_id is None:
        action_id = ''
    else:
        action_id = '"action_id":%s,' % action_id
    msg_q_tx.put(u'{"id":%s,"timestamp":%s,"type":"event","version":1,'
                 u'%s"level":"INFO","event":"%s"%s}\n' %
                 (response_id, int(((time.time() - start_time) * 100) + 3800), action_id, event, data))


def update_header(s: Session, header: str, value: str) -> bool:
    """
    Adds persistent header to Session
    :param s: Requests Session object
    :type s: Session
    :param header: Header Name
    :type header: str
    :param value: Header Value
    :type value: str
    :return: True
    :rtype: bool
    """
    s.headers.update({header: value})
    return True


def ws_connect(msg_q_rx: Queue, msg_q_tx: Queue) -> bool:
    """
    Establishes Web Socket Session
    :param msg_q_rx: WSS RX essage Queue
    :type msg_q_rx: Queue
    :param msg_q_tx: WSS TX Message Queue
    :type msg_q_tx: Queue
    :return: Web Socket session object
    :rtype: WebSocket
    """
    logger.info('CONNECTING')
    ws = WsClient(msg_q_rx, msg_q_tx)
    ws.start()
    ws_ready = False
    # Wait 15 seconds for session to establish, or error out
    for x in range(0, 16):
        if not ws.ready:
            time.sleep(1)
        else:
            ws_ready = True
            break
    if ws_ready:
        logger.info('ESTABLISHED')
        return True
    else:
        logger.error('FAILED')
        ws.stop = True
        return False
