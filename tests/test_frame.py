"""
(C) Copyright 2026
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import json

from gfutilities.service.websocket import split_frame


def test_single_object_frame():
    assert split_frame('{"a":1}') == ['{"a":1}']


def test_multi_object_frame_splits_each():
    frame = '{"id":32,"type":"log"}\n{"id":33,"type":"event"}'
    parts = split_frame(frame)
    assert len(parts) == 2
    assert [json.loads(p)['id'] for p in parts] == [32, 33]


def test_blank_lines_dropped():
    frame = '\n{"a":1}\n\n  \n{"b":2}\n'
    assert split_frame(frame) == ['{"a":1}', '{"b":2}']


def test_empty_frame_yields_nothing():
    assert split_frame('') == []
    assert split_frame('\n  \n') == []


def test_whitespace_trimmed():
    assert split_frame('   {"a":1}   ') == ['{"a":1}']
