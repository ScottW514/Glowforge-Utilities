"""
(C) Copyright 2026
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import logging

from gfutilities._common import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

# Actions that stream a pulse file and run motion.
PULS_ACTIONS = ('hunt', 'motion', 'print')
# Actions that capture a camera image and upload it.
IMAGE_ACTIONS = ('lid_image', 'head_image', 'lidar_image', 'user_image')


def dispatch_action(machine, msg: dict, allow_print: bool = True) -> str:
    """
    Route one decoded service action to the machine.

    This is the single action-surface for both cloud clients: GFUIService
    (full cloud mode, allow_print=True) and gfhome (homing only,
    allow_print=False). Every action_type the 2.6.0 service issues is
    handled here - settings, the four image captures, the three puls
    actions, update_check and factory_reset - so a machine never silently
    drops one.

    :param machine: BaseMachine (or subclass) to dispatch to
    :param msg: decoded action message
    :param allow_print: run 'print' actions (False refuses them - homing)
    :return: the action_type when a puls action was accepted for run, else
             one of 'dispatched', 'busy', 'refused', 'ignored'
    """
    action = msg.get('action_type', '')
    status = msg.get('status')

    if action == 'settings' and status == 'ready':
        machine.run_settings_report(msg)
        return 'dispatched'
    if action in IMAGE_ACTIONS:
        machine.run_capture(msg)
        return 'dispatched'
    if action in PULS_ACTIONS:
        if action == 'print' and not allow_print:
            logger.warning('refusing print action (prints not allowed here)')
            return 'refused'
        machine.run_puls(msg)
        # A puls action that was accepted is now the running action; report
        # its type so a caller pumping the protocol can track it in flight.
        if machine.running_action_id == msg.get('id'):
            return action
        return 'busy'
    if action == 'update_check':
        machine.run_update_check(msg)
        return 'dispatched'
    if action == 'factory_reset':
        machine.run_factory_reset(msg)
        return 'refused'
    logger.info('ignoring action type "%s"', action)
    return 'ignored'


__all__ = ['dispatch_action', 'PULS_ACTIONS', 'IMAGE_ACTIONS']
