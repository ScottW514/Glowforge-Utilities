"""
(C) Copyright 2026
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import json
from queue import Queue

from gfutilities.device import basemachine
from gfutilities.device.basemachine import BaseMachine


class StubMachine(BaseMachine):
    """Minimal concrete machine: records captures + settings, no hardware."""
    def __init__(self):
        BaseMachine.__init__(self)
        self.lid_captured = 0
        self.head_settings = 'unset'
        self._q_msg_tx = Queue()

    def _initialize(self):
        pass

    def _shutdown(self):
        pass

    def _button_wait(self, msg):
        pass

    def _lid_image(self, msg):
        self.lid_captured += 1

    def _head_image(self, msg, settings=None):
        self.head_settings = settings


def _events(q):
    out = []
    while not q.empty():
        out.append(json.loads(q.get())['event'])
    return out


# ---- _ok_to_run_action status handling -------------------------------------

def test_ready_starts_action():
    m = StubMachine()
    assert m._ok_to_run_action(5, 'motion', 'ready') is True
    assert m.running_action_id == 5


def test_second_ready_while_running_refused():
    m = StubMachine()
    m._ok_to_run_action(5, 'motion', 'ready')
    assert m._ok_to_run_action(6, 'motion', 'ready') is False
    assert m.running_action_id == 5


def test_non_ready_status_never_starts():
    for status in ('new', 'started', 'success', 'failure'):
        m = StubMachine()
        assert m._ok_to_run_action(5, 'motion', status) is False
        # unchanged from the idle initial (0), i.e. no action was started
        assert not m.running_action_id


def test_cancel_of_running_sets_flag():
    m = StubMachine()
    m._ok_to_run_action(5, 'motion', 'ready')
    assert m._ok_to_run_action(5, 'motion', 'cancelled') is False
    assert m._running_action_cancelled is True


def test_cancel_of_other_action_ignored():
    m = StubMachine()
    m._ok_to_run_action(5, 'motion', 'ready')
    assert m._ok_to_run_action(9, 'motion', 'cancelled') is False
    assert m._running_action_cancelled is False


# ---- user_image ------------------------------------------------------------

def test_user_image_captures_bed_and_emits_lifecycle():
    m = StubMachine()
    m.run_capture({'action_type': 'user_image', 'id': 3, 'status': 'ready'})
    m._action_thread.join(timeout=5)
    assert m.lid_captured == 1
    assert _events(m._q_msg_tx) == ['user_image:starting', 'user_image:completed']
    assert m.running_action_id is None


# ---- per-action settings normalization / plumbing (B4) ---------------------

def test_image_settings_dict_passthrough():
    assert BaseMachine._image_settings({'settings': {'LCfl': 1}}) == {'LCfl': 1}


def test_image_settings_list_takes_first():
    msg = {'settings': [{'HCil': 5}, {'HCil': 0}]}
    assert BaseMachine._image_settings(msg) == {'HCil': 5}


def test_image_settings_absent_or_empty():
    assert BaseMachine._image_settings({}) == {}
    assert BaseMachine._image_settings({'settings': None}) == {}
    assert BaseMachine._image_settings({'settings': []}) == {}


def test_lid_image_records_action_settings():
    m = StubMachine()
    m.run_capture({'action_type': 'lid_image', 'id': 4, 'status': 'ready',
                   'settings': {'LCfl': 1}})
    m._action_thread.join(timeout=5)
    assert m._action_settings == {'LCfl': 1}


def test_head_image_receives_normalized_settings():
    m = StubMachine()
    m.run_capture({'action_type': 'head_image', 'id': 5, 'status': 'ready',
                   'settings': {'HCil': 3, 'HCex': 2047}})
    m._action_thread.join(timeout=5)
    assert m.head_settings == {'HCil': 3, 'HCex': 2047}
    assert m._action_settings == {'HCil': 3, 'HCex': 2047}


def test_head_image_without_settings_passes_none():
    m = StubMachine()
    m.run_capture({'action_type': 'head_image', 'id': 6, 'status': 'ready'})
    m._action_thread.join(timeout=5)
    assert m.head_settings is None


def test_lidar_image_uses_first_settings_entry():
    m = StubMachine()
    m.run_capture({'action_type': 'lidar_image', 'id': 7, 'status': 'ready',
                   'settings': [{'HCil': 9}, {'HCil': 0}]})
    m._action_thread.join(timeout=5)
    assert m.head_settings == {'HCil': 9}


# ---- update_check ----------------------------------------------------------

def test_update_check_acknowledges_and_skips(monkeypatch):
    m = StubMachine()
    m._session = None
    probed = []
    monkeypatch.setattr(basemachine, 'firmware_check', lambda s: probed.append(True))
    m.run_update_check({'action_type': 'update_check', 'id': 8, 'status': 'ready'})
    assert probed == [True]
    assert _events(m._q_msg_tx) == [
        'firmware_update:check:starting',
        'firmware_update:check:completed',
        'firmware_update:skipping',
    ]


def test_update_check_reports_probe_failure(monkeypatch):
    m = StubMachine()
    m._session = None

    def boom(_s):
        raise RuntimeError('network down')

    monkeypatch.setattr(basemachine, 'firmware_check', boom)
    m.run_update_check({'action_type': 'update_check', 'id': 8, 'status': 'ready'})
    assert _events(m._q_msg_tx) == [
        'firmware_update:check:starting',
        'firmware_update:check:failed',
    ]


# ---- factory_reset ---------------------------------------------------------

def test_factory_reset_refused_without_action():
    m = StubMachine()
    m.run_factory_reset({'action_type': 'factory_reset', 'id': 2, 'status': 'ready'})
    assert _events(m._q_msg_tx) == ['factory_reset:cancelled']


# ---- hunt lifecycle honors a local cancel ---------------------------------

class HuntMachine(StubMachine):
    """A hunt whose child handler is aborted locally (lid, verdict, or a
    service cancel that landed mid-run) must end ':cancelled', not
    ':completed' - the service dead-reckons from that event."""
    def __init__(self, cancel):
        StubMachine.__init__(self)
        self.cancel = cancel

    def _hunt(self, msg):
        if self.cancel:
            self._running_action_cancelled = True


def test_hunt_completed_when_not_cancelled():
    m = HuntMachine(cancel=False)
    m.run_puls({'action_type': 'hunt', 'id': 7, 'status': 'ready'})
    m._action_thread.join(timeout=5)
    assert _events(m._q_msg_tx) == ['hunt:starting', 'hunt:completed']


def test_hunt_cancelled_when_handler_aborts():
    m = HuntMachine(cancel=True)
    m.run_puls({'action_type': 'hunt', 'id': 8, 'status': 'ready'})
    m._action_thread.join(timeout=5)
    assert _events(m._q_msg_tx) == ['hunt:starting', 'hunt:cancelled']
