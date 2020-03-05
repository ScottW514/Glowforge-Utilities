"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import time
import logging
from threading import Thread
from requests import Request, Response, Session
from typing import Union
from queue import Queue
from lomond import WebSocket
from lomond.persist import persist
from ..configuration import get_cfg, set_cfg

start_time = time.time()
response_id = 31


class WsClient(Thread):
    """
    Web Socket Client
    Establishes a persistent WSS client that launches a separate thread to handle WSS operations.
    Spools incoming messages to the q_rx Queue, and sends any messages placed into the q_tx Queue.
    """
    def __init__(self, q_rx: Queue, q_tx: Queue):
        """
        Class Initializer
        :param q_rx: WSS RX Message Queue
        :type q_rx: Queue
        :param q_tx: WSS TX Message Queue
        :type q_tx: Queue
        """
        self.q_rx = q_rx
        self.q_tx = q_tx
        self.stop = False
        self.ready = False
        self.ws = WebSocket(url=get_cfg('SERVICE.STATUS_SERVICE_URL') + '/' + get_cfg('SESSION.WS_TOKEN'),
                            protocols=['glowforge'], agent=get_cfg('SESSION.USER_AGENT'))
        self.ignore_events = ['ping', 'pong', 'poll', 'connecting', 'connected']
        Thread.__init__(self)

    def run(self) -> None:
        """
        Thread loop
        Listens for WS messages, and adds them the q_rx Queue.
        Monitors the q_tx, and sends any messages it finds.
        Handles PING, PONG, and POLL messages.
        :return:
        """
        for event in persist(self.ws):
            logging.info('RX-EVENT: ' + event.name)
            logging.debug(event)
            if self.stop:
                logging.info('STOP REQUESTED')
                break
            # WS reporting session is established
            if event.name == 'ready':
                self.ready = True
            # Service has sent us a text message
            elif event.name == 'text':
                logging.debug(event.text)
                self.q_rx.put(event.text)
            elif event.name not in self.ignore_events:
                logging.error('UNKNOWN RX-EVENT: ' + event.name)
            while self.ready:
                if not self.q_tx.empty():
                    send_msg = self.q_tx.get()
                    logging.info('TX-EVENT: ' + send_msg)
                    self.ws.send_text(send_msg)
                    self.q_tx.task_done()
                else:
                    break
        logging.info('CLOSING')
        self.ws.close()


def ws_connect(q_rx: Queue, q_tx: Queue) -> bool:
    """
    Establishes Web Socket Session
    :param q_rx: WSS RX essage Queue
    :type q_rx: Queue
    :param q_tx: WSS TX Message Queue
    :type q_tx: Queue
    :return: Web Socket session object
    :rtype: WebSocket
    """
    logging.info('CONNECTING')
    ws = WsClient(q_rx, q_tx)
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
        logging.info('ESTABLISHED')
        return True
    else:
        logging.error('FAILED')
        ws.stop = True
        return False


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
        logging.error('FAILED: ' + r.reason)
        return False
    else:
        return r


def download_file(s: Session, url: str, out_file: str):
    """
    Downloads file
    :param s: Requests Session object
    :type s: Session
    :param url: Target URL
    :type url: str
    :param out_file: Where to write the results
    :type out_file: str
    :return:
    """
    r = request(s, url, 'GET', stream=True)
    with open(out_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    f.close()
    return


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
    logging.info('START')
    url = get_cfg('SERVICE.SERVER_URL') + '/api/machines/%s/%s' % (msg['action_type'], msg['id'])
    headers = {'Content-Type': 'image/jpeg'}
    r = request(s, url, 'POST', data=img, headers=headers)
    logging.debug(r.json)
    if not r:
        return False
    logging.info('COMPLETE')
    return True


def send_wss_event(q_tx, msg, event, **kwargs):
    global response_id
    global start_time
    response_id += 1

    if 'data' in kwargs:
        data = ',"%s":%s' % (kwargs['data']['key'], kwargs['data']['value'])
    else:
        data = ''
    q_tx.put(u'{"id":%s,"timestamp":%s,"type":"event","version":1,'
             u'"action_id":%s,"level":"INFO","event":"%s"%s}\n' %
             (response_id, int(((time.time() - start_time) * 100) + 3800), msg['id'], event, data))


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
    logging.info('CHECKING')
    r = request(s, get_cfg('SERVICE.SERVER_URL') + '/update/current', 'GET')
    if not r:
        logging.error('FAILED')
        return False
    rj = r.json()
    logging.debug(rj)
    if not rj['version'] == get_cfg('MACHINE.FIRMWARE'):
        logging.info('New Firmware Available: Installed (%s), Available (%s)'
                     % (get_cfg('MACHINE.FIRMWARE'), rj['version']))
        return rj
    else:
        logging.info('LATEST ALREADY INSTALLED.')
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
    logging.info('DOWNLOADING')
    download_file(s, fw['download_url'], '%s/glowforge-fw-v%s.fw' % (get_cfg('GENERAL.FIRMWARE_DIR'), fw['version']))
    logging.info('COMPLETE.')
    return True


def get_session() -> Session:
    """
    Creates web api session object.
    :return: Requests Session object
    :rtype: Session
    """
    s = Session()
    set_cfg('SESSION.USER_AGENT', 'OpenGlow/%s' % get_cfg('MACHINE.FIRMWARE'))
    s.headers.update({'user-agent': get_cfg('SESSION.USER_AGENT')})
    logging.debug('Returning object : %s' % s)
    return s
