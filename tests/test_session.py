# -*- coding: UTF-8 -*-
from rogertalk import RogerTalk

DEV_SETTINGS = {
    'ROGERTALK_DEVELOPMENT': True,
    'ROGERTALK_DEMO': True,
    'ROGERTALK_TOKEN': '12345',
}

PROD_SETTINGS = DEV_SETTINGS.copy()
PROD_SETTINGS.update({
    'ROGERTALK_DEVELOPMENT': False,
    'ROGERTALK_DEMO': False,
})

sp_dev = RogerTalk(settings=DEV_SETTINGS)
sp_prod = RogerTalk(settings=PROD_SETTINGS)


def test_dev_settings():
    assert sp_dev.session.__class__.__name__ == 'DevelopmentSession'
    assert sp_dev.session.site == 'https://api.rogertalk.com/'
    assert sp_prod.session.token is '12345'
    assert sp_prod.session.language is 'en_US'
    assert sp_dev.session.is_development is True
    assert sp_dev.session.is_demo is True


def test_prod_settings():
    assert sp_prod.session.__class__.__name__ == 'Session'
    assert sp_prod.session.site == 'https://api.rogertalk.ag/'
    assert sp_prod.session.token is '12345'
    assert sp_prod.session.language is 'en_US'
    assert sp_prod.session.is_development is False
    assert sp_prod.session.is_demo is False


def test_prod_settings_with_demo_true():
    prod_settings = DEV_SETTINGS.copy()
    prod_settings.update({
        'ROGERTALK_DEVELOPMENT': False,
        'ROGERTALK_DEMO': True,
    })

    subject = RogerTalk(settings=prod_settings)
    assert subject.session.__class__.__name__ == 'Session'
    assert subject.session.site == 'https://api.rogertalk.ag/'
    assert sp_prod.session.token is '12345'
    assert sp_prod.session.language is 'en_US'
    assert subject.session.is_development is False
    assert subject.session.is_demo is True


def test_prod_settings_with_language_german():
    prod_settings = DEV_SETTINGS.copy()
    prod_settings.update({
        'ROGERTALK_DEVELOPMENT': False,
        'ROGERTALK_DEMO': True,
        'ROGERTALK_LANGUAGE': 'de_DE',
    })

    subject = RogerTalk(settings=prod_settings)
    assert subject.session.__class__.__name__ == 'Session'
    assert subject.session.site == 'https://api.rogertalk.ag/'
    assert subject.session.token is '12345'
    assert subject.session.language is 'de_DE'
    assert subject.session.is_development is False
    assert subject.session.is_demo is True
