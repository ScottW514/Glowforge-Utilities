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
    along with GF-Library.  If not, see <http://www.gnu.org/licenses/>.


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

