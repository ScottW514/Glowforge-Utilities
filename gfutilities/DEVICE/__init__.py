"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
__all__ = ['actions', 'authentication', 'configuration', 'connection', 'emulator', 'web_api', 'ws_api', 'websocket']

"""
_ACTIONS {dict} holds the sequence of MACHINE responses/actions for each action commanded by the SERVICE
    Actions organized by name, group number, and finally action number. Typically, all actions in a group are processed
    together.  Groups may be ran individually, or as a batch in sequential order - determinied by the function running
    them.
    api_function_name{str}: The name of the api function these actions belong to.
        {dict}
            group{int}: A numbered group of actions, beginning at 0.
                {dict}
                    action{int}: The number of the action, in order beginning at 0.
                        delay: {float} (Required) Amount of time to pause before
                                                  sending response or executing the action, in seconds.
                        act: {bool} (Required) Whether or not this action is currently active.
                                               Set to True to execute, False to skip.
                        api: {str} (Required) The API.  'web' for 'web_api', 'ws' for 'ws_api'.
                        run: {str} (Required) The API command to run.
                        msg: {str} (Required, but can be empty for some actions)
"""
_ACTIONS = {
    'firmware_check':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'web', 'run': 'event', 'msg': '{"local": "<MACHINE.FIRMWARE>", "type": "event", "id": <MILLI_EPOCH>, "event": "firmware_update:check:starting"}'},
        },
         1: {
            0: {'delay': 0, 'act': True, 'api': 'web', 'run': 'event', 'msg': '{"remote": "<AVAILABLE_FIRMWARE>", "local": "<MACHINE.FIRMWARE>", "type": "event", "id": <MILLI_EPOCH>, "event": "firmware_update:check:complete"}'},
        },
         2: {
            0: {'delay': 0, 'act': True, 'api': 'web', 'run': 'event', 'msg': '{"version": "<AVAILABLE_FIRMWARE>", "type": "event", "id": <MILLI_EPOCH>, "event": "firmware_update:skipping"}'},
        }
        },
    'settings':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'web', 'run': 'status', 'msg': ''},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"settings:received","log":"state=ready","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"settings:starting","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"settings:completed","settings":{"values":<SETTINGS>},"level":"INFO"}'},
            4: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"settings:reset","level":"INFO"}'}
        }
        },
    'hunt':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:received","log":"state=ready","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:starting","level":"INFO"}'},
        },
         1: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:homing:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"estop:deactivated","log":"ESTOP deactivated","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:idle:succeeded","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:warmup:starting","level":"INFO"}'},
            4: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:warmup:succeeded","level":"INFO"}'},
            5: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:starting:starting","level":"INFO"}'},
            6: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:running","level":"INFO"}'},
            7: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:starting:succeeded","level":"INFO"}'},
            8: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:running:starting","level":"INFO"}'},
        },
         2: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:running:succeeded","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:finished:starting","level":"INFO"}'},
        },
         3: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:finished:succeeded","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:resting:starting","level":"INFO"}'},

        },
         4: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"hunt:reset","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":":resting:succeeded","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":":idle:starting","level":"INFO"}'},
        },
         5: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"estop:activated","log":"ESTOP activated","level":"INFO"}'},
        }
        },
    'lid_image':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:received","log":"state=ready","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:starting","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:capture:starting","level":"INFO"}'},
        },
         1: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:capture:completed","log":"capture time: 1.47755","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:upload:starting","level":"INFO"}'},
        },
         2: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:upload:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:completed","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lid_image:reset","level":"INFO"}'},
        }
        },
    'motion':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:received","log":"state=ready","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:starting","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:download:starting","log":"downloading pulse data from <MOTION_URL>","level":"INFO"}'},
        },
         1: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:download:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"estop:deactivated","log":"ESTOP deactivated","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:idle:succeeded","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:warmup:starting","level":"INFO"}'},
            4: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:warmup:succeeded","level":"INFO"}'},
            5: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:starting:starting","level":"INFO"}'},
            6: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:running","level":"INFO"}'},
            7: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:starting:succeeded","level":"INFO"}'},
            8: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:running:starting","level":"INFO"}'},
        },
         2: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:running:succeeded","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:finished:starting","level":"INFO"}'},
        },
         3: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:finished:succeeded","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:resting:starting","level":"INFO"}'},
        },
         4: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"motion:reset","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":":resting:succeeded","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":":idle:starting","level":"INFO"}'},
        },
         5: {
            0: {'delay': .5, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"estop:activated","log":"ESTOP activated","level":"INFO"}'},
        }
        },
    'head_image':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:received","log":"state=ready","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:starting","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:capture:starting","level":"INFO"}'},
        },
         1: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:capture:completed","log":"capture time: 2.514","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:upload:starting","level":"INFO"}'},
        },
         2: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:upload:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:completed","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"head_image:reset","level":"INFO"}'},
        }
        },
    'lidar_image':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:received","log":"state=ready","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:starting","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:capture:starting","level":"INFO"}'},
        },
         1: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:capture:completed","log":"capture time: 2.514","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:upload:starting","level":"INFO"}'},
        },
         2: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:upload:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:completed","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"lidar_image:reset","level":"INFO"}'},
        }
        },
    'print':
        {0: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:received","log":"state=ready","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:starting","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:download:starting","log":"downloading pulse data from <MOTION_URL>","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'progress', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"progress","version":1,"action_id":<ACTION_ID>,"progress":"print:download","current":0,"units":"bytes"}'},
        },
         1: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:download:completed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:waiting","log":"waiting for button press","level":"INFO"}'},
        },
         2: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"button:pressed","log":"button pressed","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:idle:succeeded","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:warmup:starting","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:warmup:succeeded","level":"INFO"}'},
            4: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:starting:starting","level":"INFO"}'},
            5: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:running","level":"INFO"}'},
            6: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:starting:succeeded","level":"INFO"}'},
            7: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:running:starting","level":"INFO"}'},
        },
         3: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"estop:deactivated","log":"ESTOP deactivated","level":"INFO"}'},
        },
         4: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"button:released","log":"button released","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:running:succeeded","level":"INFO"}'},
        },
         5: {
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:finished:starting","level":"INFO"}'},
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:finished:succeeded","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:return_to_home:starting","level":"INFO"}'},
        },
         6: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:return_to_home:succeeded","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:resting:starting","level":"INFO"}'},
        },
         7: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:resting","level":"INFO"}'},
        },
         8: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":"estop:activated","log":"ESTOP activated","level":"INFO"}'},
            1: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:completed","level":"INFO"}'},
            2: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"action_id":<ACTION_ID>,"event":"print:reset","level":"INFO"}'},
            3: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":":resting:succeeded","level":"INFO"}'},
         },
         9: {
            0: {'delay': 0, 'act': True, 'api': 'ws', 'run': 'event', 'msg': '{"id":<ID>,"timestamp":<TIMESTAMP>,"type":"event","version":1,"event":":idle:starting","level":"INFO"}'},
        },
        },
}


"""
_STATES{dict}: Used for tracking various stateful details.
"""
_STATES = {
    'homing': 1,        # The current step in the homing process.
    'last_action': ''   # Name of the action processed.
}
