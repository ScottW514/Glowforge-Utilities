"""
Copyright 2017 Scott Wiederhold
This file is part of GF-Library.

    GF-Library is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GF-Library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GF-Library.  If not, see <http://www.gnu.org/licenses/>.


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
