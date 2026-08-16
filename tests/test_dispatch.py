"""
(C) Copyright 2026
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
from gfutilities.service.dispatch import dispatch_action, PULS_ACTIONS, IMAGE_ACTIONS


class FakeMachine:
    """Records which run_* entry point the dispatcher called."""
    def __init__(self, accept_puls=True):
        self.calls = []
        self.running_action_id = None
        self._accept_puls = accept_puls

    def run_settings_report(self, msg):
        self.calls.append(('settings', msg['id']))

    def run_capture(self, msg):
        self.calls.append(('capture', msg['action_type']))

    def run_puls(self, msg):
        self.calls.append(('puls', msg['action_type']))
        if self._accept_puls:
            self.running_action_id = msg['id']

    def run_update_check(self, msg):
        self.calls.append(('update_check', msg['id']))

    def run_factory_reset(self, msg):
        self.calls.append(('factory_reset', msg['id']))


def _msg(action, status='ready', mid=1, **extra):
    m = {'action_type': action, 'status': status, 'id': mid}
    m.update(extra)
    return m


def test_settings_ready_routes_to_report():
    m = FakeMachine()
    assert dispatch_action(m, _msg('settings')) == 'dispatched'
    assert m.calls == [('settings', 1)]


def test_settings_non_ready_ignored():
    m = FakeMachine()
    assert dispatch_action(m, _msg('settings', status='success')) == 'ignored'
    assert m.calls == []


def test_all_image_actions_route_to_capture():
    for action in IMAGE_ACTIONS:
        m = FakeMachine()
        assert dispatch_action(m, _msg(action)) == 'dispatched'
        assert m.calls == [('capture', action)]


def test_user_image_is_an_image_action():
    assert 'user_image' in IMAGE_ACTIONS


def test_puls_accepted_returns_action_type():
    for action in ('hunt', 'motion', 'print'):
        m = FakeMachine(accept_puls=True)
        assert dispatch_action(m, _msg(action, mid=7)) == action


def test_puls_busy_returns_busy():
    m = FakeMachine(accept_puls=False)
    assert dispatch_action(m, _msg('motion')) == 'busy'


def test_print_refused_when_not_allowed():
    m = FakeMachine()
    assert dispatch_action(m, _msg('print'), allow_print=False) == 'refused'
    # run_puls must not have been called at all
    assert m.calls == []


def test_hunt_and_motion_allowed_when_print_disallowed():
    for action in ('hunt', 'motion'):
        m = FakeMachine()
        assert dispatch_action(m, _msg(action), allow_print=False) == action


def test_update_check_routed():
    m = FakeMachine()
    assert dispatch_action(m, _msg('update_check')) == 'dispatched'
    assert m.calls == [('update_check', 1)]


def test_factory_reset_refused():
    m = FakeMachine()
    assert dispatch_action(m, _msg('factory_reset')) == 'refused'
    assert m.calls == [('factory_reset', 1)]


def test_unknown_action_ignored():
    m = FakeMachine()
    assert dispatch_action(m, _msg('telemetry_blob')) == 'ignored'
    assert m.calls == []


def test_missing_action_type_ignored():
    m = FakeMachine()
    assert dispatch_action(m, {'id': 1, 'status': 'ready'}) == 'ignored'


def test_puls_actions_constant_matches_expected():
    assert PULS_ACTIONS == ('hunt', 'motion', 'print')
