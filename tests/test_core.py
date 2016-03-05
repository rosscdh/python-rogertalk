# -*- coding: UTF-8 -*-
from rogertalk import RogerTalk

DEV_SETTINGS = {
    'ROGERTALK_DEVELOPMENT': True,
    'ROGERTALK_DEMO': True,
    'ROGERTALK_TOKEN': '12345',
}

subject = RogerTalk(settings=DEV_SETTINGS)


def test_wrap_namespace():
    """
    Test we have the correct data structure
    """
    resp = subject.payment().wrap_namespace(my='test', keywords='here')
    assert resp == '{"data": {"keywords": "here", "demo": 1, "apikey": "12345", "my": "test"}}'


def test_headers():
    assert subject.payment().headers() == {'Accept': 'application/json;', 'Content-Type': 'application/json; charset=utf-8;'}
