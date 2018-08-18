"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

TODO: Error checking/handling of some kind
"""
from . import web_api, ws_api
import logging


def run_action(api, action, **kwargs):
    """
    Runs API action
    :param api: {str} API
    :param action: {str} API action
    :param kwargs:
    :return:
    """
    logging.debug('RUNNING %s:%s' % (api, action))
    if api == 'web':
        return web_api.run_cmd(action, **kwargs)
    elif api == 'ws':
        return ws_api.run_cmd(action, **kwargs)
    else:
        logging.error('UNKNOWN %s:%s' % (api, action))
        return False
