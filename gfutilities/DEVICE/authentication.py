"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from .connection import request
from .connection import update_header
import logging


def authenticate_machine(s, cfg):
    """
    Authenticates machine to service.
    POSTS serial number prefixed with an S and machine password to <server_url>/machines/sign_in.
    On success, server responds with JSON encoded 'ws_token' for WSS auth, and 'auth_token' that is
    added as a header to all session web API requests.
    Auth token header is 'Authorization': 'Bearer <auth_token>'
    :param s: {Session} Emulator session object.
    :param cfg: {dict} Emulator configuration dictionary.
    :return: {bool} Authentication result.
    """
    logging.info('START')
    r = request(s, cfg['SERVICE.SERVER_URL'] + '/machines/sign_in', 'POST',
                data={'serial': 'S' + str(cfg['MACHINE.SERIAL']), 'password': cfg['MACHINE.PASSWORD']})
    if r:
        rj = r.json()
        logging.debug(rj)
        cfg['SESSION.WS_TOKEN'] = rj['ws_token']
        cfg['SESSION.AUTH_TOKEN'] = rj['auth_token']
        update_header(s, 'Authorization', "Bearer %s" % cfg['SESSION.AUTH_TOKEN'])
        logging.info('SUCCESS')
        return True
    else:
        logging.error('FAILED')
        return False

