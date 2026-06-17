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
import requests
from requests import Request, Response, Session
from threading import Thread
import time
from typing import Union

import websocket

from gfutilities._common import *
from gfutilities.configuration import get_cfg, set_cfg
from gfutilities.puls import decode_all_steps

start_time = time.time()
response_id = 31

logger = logging.getLogger(LOGGER_NAME)


class WsClient(Thread):
    """
    Web Socket Client
    Establishes a persistent WSS client that runs the WebSocket event loop in a separate thread.
    Incoming text messages are spooled to the q_msg_rx Queue; messages placed into the q_msg_tx
    Queue are sent out by a dedicated transmit-pump thread.
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
        self.ws = websocket.WebSocketApp(
            get_cfg('SERVICE.STATUS_SERVICE_URL') + '/' + get_cfg('SESSION.WS_TOKEN'),
            header={'User-Agent': get_cfg('SESSION.USER_AGENT')},
            subprotocols=['glowforge'],
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        Thread.__init__(self)

    def _on_open(self, _ws) -> None:
        """WS handshake complete - ready to send/receive."""
        logger.info('RX-EVENT: ready')
        self.ready = True

    def _on_message(self, _ws, message) -> None:
        """Service sent us a message. Text frames arrive as str, binary frames as bytes."""
        if isinstance(message, (bytes, bytearray)):
            logger.error('UNEXPECTED BINARY RX-EVENT (%s bytes)' % len(message))
            return
        logger.debug(message)
        self.msg_q_rx.put(message)

    def _on_error(self, _ws, error) -> None:
        logger.error('RX-EVENT: error: %s' % error)

    def _on_close(self, _ws, status_code, msg) -> None:
        self.ready = False
        logger.info('RX-EVENT: closed (%s, %s)' % (status_code, msg))

    def run(self) -> None:
        """
        Thread loop.
        Starts the transmit pump, then runs the WebSocket event loop, reconnecting
        automatically until stop is requested.
        :return:
        """
        Thread(target=self._tx_pump, daemon=True).start()
        # reconnect: auto-retry the connection every 5s (the service drops it frequently).
        # ping_interval: keep the connection alive (the service speaks standard WS ping/pong).
        self.ws.run_forever(reconnect=5, ping_interval=30, ping_timeout=10)
        logger.info('CLOSING')

    def _tx_pump(self) -> None:
        """
        Drains the transmit queue and sends messages while the socket is open.
        Runs until stop is requested, then closes the socket so run_forever() returns.
        :return:
        """
        while not self.stop:
            if self.ready and not self.msg_q_tx.empty():
                send_msg = self.msg_q_tx.get()
                logger.info('TX-EVENT: ' + send_msg.strip())
                try:
                    self.ws.send(send_msg)
                except websocket.WebSocketException as e:
                    logger.error('TX FAILED: %s' % e)
                self.msg_q_tx.task_done()
            else:
                time.sleep(0.1)
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
    endpoint = msg.get('endpoint')
    if endpoint:
        # v2.6.0+ protocol: the service supplies a presigned storage URL in the
        # action's "endpoint" field and the image is uploaded straight to it.
        # The presigned URL carries its own auth, so it must NOT go through the
        # authenticated Glowforge session (a Bearer header makes GCS reject it);
        # PUT the raw bytes with a plain request.
        r = requests.put(endpoint, data=img, headers={'Content-Type': 'image/jpeg'}, timeout=30)
        ok = r.status_code in (200, 201, 204)
    else:
        # Legacy fallback: POST to the app server (pre-2.6.0 behaviour).
        url = get_cfg('SERVICE.SERVER_URL') + '/api/machines/%s/%s' % (msg['action_type'], msg['id'])
        r = request(s, url, 'POST', data=img, headers={'Content-Type': 'image/jpeg'})
        ok = bool(r)
    if not ok:
        logger.error('FAILED: %s %s' % (getattr(r, 'status_code', '?'), getattr(r, 'reason', '')))
        return False
    logger.debug('upload response: %s' % r)
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
        total_header = _byte_to_int(puls_data[4:8])
        # iter_content() only guarantees *up to* chunk_size bytes per chunk, and the
        # header has grown past 1 KB on newer firmware, so it can span several chunks.
        # Buffer until the whole header is present before parsing it.
        while len(puls_data) < total_header:
            try:
                puls_data += next(res)
            except StopIteration:
                logger.error('puls file ended before header was complete')
                return False
        info['header_len'] = total_header - 8
        pos = 8
        while pos < total_header:
            info['header_data'][puls_data[pos:pos + 4].decode()] = _byte_to_int(puls_data[pos + 4:pos + 8])
            pos += 8
        size = len(puls_data[pos:])
        stat = decode_all_steps(puls_data[pos:])
        # TODO: REMOVE THIS TEMP RAW WRITE - ONLY FOR QUICK TESTING
        base_file_name = '%s/%s' % (str(Path(get_cfg('LOGGING.FILE')).parent), time.strftime("%Y-%m-%d_%H%M%S"))
        raw = open(base_file_name + '.puls', 'wb')
        raw.write(puls_data)
        f.write(puls_data[pos:])
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
