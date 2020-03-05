"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import logging
from requests import Session
from .websocket import request, update_header
from ..configuration import get_cfg, set_cfg


def authenticate_machine(s: Session) -> bool:
    """
    Authenticates machine to service.
    POSTS serial number prefixed with an S and machine password to <server_url>/machines/sign_in.
    On success, server responds with JSON encoded 'ws_token' for WSS auth, and 'auth_token' that is
    added as a header to all session web API requests.
    Auth token header is 'Authorization': 'Bearer <auth_token>'
    :param s: Emulator session object.
    :type s: Session
    :return: Authentication result.
    :rtype: bool
    """
    logging.info('START')
    r = request(s, get_cfg('SERVICE.SERVER_URL') + '/machines/sign_in', 'POST',
                data={'serial': 'S' + str(get_cfg('MACHINE.SERIAL')), 'password': get_cfg('MACHINE.PASSWORD')})
    if r:
        rj = r.json()
        logging.debug(rj)
        set_cfg('SESSION.WS_TOKEN', rj['ws_token'])
        set_cfg('SESSION.AUTH_TOKEN', rj['auth_token'])
        update_header(s, 'Authorization', "Bearer %s" % get_cfg('SESSION.AUTH_TOKEN'))
        logging.info('SUCCESS')
        return True
    else:
        logging.error('FAILED')
        return False

