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
import requests
import logging


def download_file(s, url, out_file):
    """
    Downloads file
    :param s: {Session} Requests Session object
    :param url: {str} Target URL
    :param out_file: {str} Where to write the results
    :return:
    """
    r = request(s, url, 'GET', stream=True)
    with open(out_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    f.close()
    return


def get_session(cfg):
    """
    Creates web api session object.
    :param cfg: {dict} Emulator's configuration dictionary.
    :return: {Session} Requests Session object
    """
    s = requests.Session()
    cfg['SESSION.USER_AGENT'] = 'Glowforge/%s' % cfg['MACHINE.FIRMWARE']
    s.headers.update({'user-agent': cfg['SESSION.USER_AGENT']})
    logging.debug('Returning object : %s' % s)
    return s


def request(s, url, method, timeout=15, stream=False, **kwargs):
    """
    Submits requests to provided url using the established Session object
    :param s: {Session} Requests Session object
    :param url: {str} Target URL
    :param method: {str} Method for the request
    :param timeout: {int} Timeout
    :param stream: {bool} Stream
    :param kwargs:
    :return: {Response} Requests Response object, or False on error.
    """
    req = requests.Request(method, str.replace(str(url), 'wss://', 'https://'), **kwargs)
    req = s.prepare_request(req)
    r = s.send(req, stream=stream, timeout=timeout)
    if r.status_code != 200:
        logging.error('FAILED: ' + r.reason)
        return False
    else:
        return r


def update_header(s, header, value):
    """
    Adds persistent header to Session
    :param s: {Session} Requests Session object
    :param header: {str} Header Name
    :param value: {str} Header Value
    :return: {bool} True
    """
    s.headers.update({header: value})
    return True


