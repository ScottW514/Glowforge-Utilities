"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT

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
    cfg['SESSION.USER_AGENT'] = 'OpenGlow/%s' % cfg['MACHINE.FIRMWARE']
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


