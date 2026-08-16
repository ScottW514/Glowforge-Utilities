"""
(C) Copyright 2026
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from io import BytesIO
from queue import Queue

import pytest

from gfutilities.configuration import set_cfg
from gfutilities.service import websocket as ws


# ---- C1: reconnect with a fresh ws_token -----------------------------------

class _FakeWSApp:
    """Records constructed URLs; run_forever returns immediately (closed)."""
    urls = []

    def __init__(self, url, **kw):
        _FakeWSApp.urls.append(url)
        self.on_open = kw.get('on_open')

    def run_forever(self, **kw):
        return None

    def close(self):
        pass

    def send(self, m):
        pass


def _ws_cfg():
    set_cfg('SERVICE.STATUS_SERVICE_URL', 'wss://status.example')
    set_cfg('SESSION.WS_TOKEN', 'TOKEN')
    set_cfg('SESSION.USER_AGENT', 'ua')


def test_build_url_uses_current_token(monkeypatch):
    _ws_cfg()
    monkeypatch.setattr('websocket.WebSocketApp', _FakeWSApp)
    _FakeWSApp.urls = []
    c = ws.WsClient(Queue(), Queue())
    c._build()
    assert _FakeWSApp.urls[-1] == 'wss://status.example/TOKEN'


def test_reconnect_reauths_for_fresh_token(monkeypatch):
    _ws_cfg()
    monkeypatch.setattr('websocket.WebSocketApp', _FakeWSApp)
    _FakeWSApp.urls = []
    reauth = []
    monkeypatch.setattr('gfutilities.service.authentication.authenticate_machine',
                        lambda s: (reauth.append(s), True)[1])
    c = ws.WsClient(Queue(), Queue(), session=object())

    calls = {'n': 0}

    def fake_sleep(_secs):
        calls['n'] += 1
        if calls['n'] >= 2:      # stop during the 2nd reconnect wait
            c.stop = True
            return True
        return False

    monkeypatch.setattr(c, '_sleep_or_stop', fake_sleep)
    c.run()
    # first connect (no re-auth) + 1 reconnect (re-auth) before stop
    assert len(_FakeWSApp.urls) == 2
    assert len(reauth) == 1


def test_no_session_never_reauths(monkeypatch):
    _ws_cfg()
    monkeypatch.setattr('websocket.WebSocketApp', _FakeWSApp)
    _FakeWSApp.urls = []
    reauth = []
    monkeypatch.setattr('gfutilities.service.authentication.authenticate_machine',
                        lambda s: reauth.append(s))
    c = ws.WsClient(Queue(), Queue(), session=None)
    calls = {'n': 0}

    def fake_sleep(_secs):
        calls['n'] += 1
        c.stop = True
        return True

    monkeypatch.setattr(c, '_sleep_or_stop', fake_sleep)
    c.run()
    assert reauth == []


def test_sleep_or_stop_returns_on_stop():
    c = ws.WsClient(Queue(), Queue())
    c.stop = True
    assert c._sleep_or_stop(5) is True


# ---- C2: 401 -> re-auth -> replay ------------------------------------------

class _Resp:
    def __init__(self, code):
        self.status_code = code
        self.reason = 'r'


class _Sess:
    def __init__(self, codes):
        self._codes = list(codes)
        self.sent = 0

    def prepare_request(self, req):
        return req

    def send(self, req, **kw):
        self.sent += 1
        return _Resp(self._codes.pop(0))


def test_request_401_reauths_and_replays(monkeypatch):
    s = _Sess([401, 200])
    reauth = []
    monkeypatch.setattr('gfutilities.service.authentication.authenticate_machine',
                        lambda sess: (reauth.append(sess), True)[1])
    r = ws.request(s, 'https://app.example/x', 'GET')
    assert r.status_code == 200
    assert s.sent == 2          # original + one replay
    assert reauth == [s]


def test_request_no_replay_when_disabled(monkeypatch):
    s = _Sess([401])
    reauth = []
    monkeypatch.setattr('gfutilities.service.authentication.authenticate_machine',
                        lambda sess: reauth.append(sess))
    r = ws.request(s, 'https://app.example/sign_in', 'POST', _retry_auth=False)
    assert r is False
    assert reauth == []         # sign-in must never trigger re-auth (no recursion)


def test_request_reauth_failure_gives_up(monkeypatch):
    s = _Sess([401, 401])
    monkeypatch.setattr('gfutilities.service.authentication.authenticate_machine',
                        lambda sess: True)
    r = ws.request(s, 'https://app.example/x', 'GET')
    assert r is False           # replay also 401 -> False, no infinite loop
    assert s.sent == 2


# ---- C4: load_motion disk-filler + oversize handling -----------------------

def _fake_puls(body: bytes) -> bytes:
    # \x00 G F 1 | header_len(16, little-endian) | 'STfr' + 10000 | body
    header = b'\x00GF1' + (16).to_bytes(4, 'little') + b'STfr' + (10000).to_bytes(4, 'little')
    return header + body


class _StreamResp:
    def __init__(self, data):
        self._data = data

    def iter_content(self, chunk_size=1024):
        for i in range(0, len(self._data), chunk_size):
            yield self._data[i:i + chunk_size]


def test_load_motion_writes_body_and_no_disk_filler(tmp_path, monkeypatch):
    set_cfg('LOGGING.DIR', str(tmp_path / 'log'))
    (tmp_path / 'log').mkdir()
    set_cfg('LOGGING.SAVE_PULS', None)
    body = bytes(range(100)) * 3
    monkeypatch.setattr(ws, 'request', lambda *a, **k: _StreamResp(_fake_puls(body)))
    out = BytesIO()
    info = ws.load_motion(None, 'http://x', out)
    assert out.getvalue() == body
    assert info['size'] == len(body)
    # nothing dumped into the log dir
    assert list((tmp_path / 'log').glob('*.puls')) == []
    assert list((tmp_path / 'log').glob('*.info')) == []


def test_load_motion_save_puls_flag_writes_debug_copy(tmp_path, monkeypatch):
    set_cfg('LOGGING.DIR', str(tmp_path / 'log'))
    (tmp_path / 'log').mkdir()
    set_cfg('LOGGING.SAVE_PULS', True)
    body = bytes(range(50))
    monkeypatch.setattr(ws, 'request', lambda *a, **k: _StreamResp(_fake_puls(body)))
    ws.load_motion(None, 'http://x', BytesIO())
    assert list((tmp_path / 'log').glob('*.puls'))
    assert list((tmp_path / 'log').glob('*.info'))
    set_cfg('LOGGING.SAVE_PULS', None)


# ---- D1a: GFUIService stoppable --------------------------------------------

class _FakeMachine:
    def __init__(self):
        self.started = False
        self.stopped = False

    def start(self, session, q_tx):
        self.started = True

    def stop(self):
        self.stopped = True


def test_gfuiservice_stops_and_safes_machine():
    from gfutilities.service.gfuiservice import GFUIService
    m = _FakeMachine()
    svc = GFUIService(m)
    svc.stop = True                 # request stop before entering the loop
    svc.run()
    assert m.started and m.stopped   # machine.stop() runs -> hardware safed


def test_request_stop_breaks_running_loop():
    import threading
    import time
    from gfutilities.service.gfuiservice import GFUIService
    m = _FakeMachine()
    svc = GFUIService(m)
    t = threading.Thread(target=svc.run)
    t.start()
    time.sleep(0.2)                 # loop is spinning on the timeout get
    svc.request_stop()
    t.join(timeout=3)
    assert not t.is_alive()
    assert m.stopped


# ---- E1 finding 2: no thread may outlive a clean stop ----------------------

class _BlockingWSApp:
    """run_forever connects (on_open) then blocks until close()."""
    def __init__(self, url, **kw):
        import threading
        self._on_open = kw.get('on_open')
        self._closed = threading.Event()

    def run_forever(self, **kw):
        self._on_open(self)
        self._closed.wait(10)

    def close(self):
        self._closed.set()

    def send(self, m):
        pass


def test_ws_client_is_daemon():
    assert ws.WsClient(Queue(), Queue()).daemon


def test_action_thread_is_daemon():
    from gfutilities.device.basemachine import _ActionThread
    assert _ActionThread(None, {}).daemon


def test_ws_connect_returns_stoppable_client(monkeypatch):
    _ws_cfg()
    monkeypatch.setattr('websocket.WebSocketApp', _BlockingWSApp)
    c = ws.ws_connect(Queue(), Queue())
    assert isinstance(c, ws.WsClient)
    assert c.ready
    assert c.shutdown(timeout=5)
    assert not c.is_alive()


def test_gfuiservice_connect_keeps_ws_reference(monkeypatch):
    from gfutilities.service import gfuiservice
    sentinel = object()
    monkeypatch.setattr(gfuiservice, 'get_session', lambda: object())
    monkeypatch.setattr(gfuiservice, 'authenticate_machine', lambda s: True)
    monkeypatch.setattr(gfuiservice, 'ws_connect', lambda rx, tx, s: sentinel)
    set_cfg('FACTORY_FIRMWARE.CHECK', None)
    svc = gfuiservice.GFUIService(_FakeMachine())
    assert svc.connect() is True
    assert svc._ws is sentinel


def test_gfuiservice_run_shuts_down_ws_client():
    from gfutilities.service.gfuiservice import GFUIService

    class _FakeWs:
        ready = False

        def __init__(self):
            self.down = False

        def shutdown(self, timeout=10):
            self.down = True
            return True

    m = _FakeMachine()
    svc = GFUIService(m)
    fake = _FakeWs()
    svc._ws = fake
    svc.stop = True
    svc.run()
    assert m.stopped
    assert fake.down
    assert svc._ws is None


def test_load_motion_reraises_ring_full(monkeypatch):
    set_cfg('LOGGING.SAVE_PULS', None)
    monkeypatch.setattr(ws, 'request', lambda *a, **k: _StreamResp(_fake_puls(bytes(200))))

    class _RingFull:
        def write(self, _b):
            raise OSError(12, 'Cannot allocate memory')  # -ENOMEM

    with pytest.raises(OSError):
        ws.load_motion(None, 'http://x', _RingFull())
