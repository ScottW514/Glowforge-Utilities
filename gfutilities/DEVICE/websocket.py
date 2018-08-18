"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from lomond import WebSocket
from lomond.persist import persist
import threading
import time
import logging


class WsClient(threading.Thread):
    """
    Web Socket Client
    Establishes a persistent WSS client that launches a separate thread to handle WSS operations.
    Spools incoming messages to the q_rx Queue, and sends any messages placed into the q_tx Queue.
    """
    def __init__(self, cfg, q):
        """
        Class Initializer
        :param cfg: {dict} Emulator's configuration dictionary
        :param q: {Queue} WSS RX/TX Message Queue
        """
        self.q_rx = q['rx']
        self.q_tx = q['tx']
        self.stop = False
        self.ready = False
        self.ws = WebSocket(url=cfg['SERVICE.STATUS_SERVICE_URL'] + '/' + cfg['SESSION.WS_TOKEN'],
                            protocols=['glowforge'], agent=cfg['SESSION.USER_AGENT'])
        self.ignore_events = ['ping', 'pong', 'poll', 'connecting', 'connected']
        threading.Thread.__init__(self)

    def run(self):
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


def ws_connect(cfg, q):
    """
    Establishes Web Socket Session
    :param cfg: {dict} Emulator's configuration dictionary
    :param q: {Queue} WSS RX/TX Message Queue
    :return: {WebSocket} Web Socket session object
    """
    logging.info('CONNECTING')
    ws = WsClient(cfg, q)
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

