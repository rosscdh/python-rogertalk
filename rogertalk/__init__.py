# -*- coding: UTF-8 -*-
from rogertalk.core import Session
from rogertalk.core import BaseApi
from rogertalk.api import Stream


def get_session(settings):
    if type(settings) is dict:
        client_id = settings.get('ROGERTALK_CLIENT_ID', None)
        client_secret = settings.get('ROGERTALK_CLIENT_SECRET', None)
    else:
        client_id = getattr(settings, 'ROGERTALK_CLIENT_ID', None)
        client_secret = getattr(settings, 'ROGERTALK_CLIENT_SECRET', None)

    assert client_id is not None, 'You must provide a ROGERTALK_CLIENT_ID in the settings passed into rogertalk.get_session(settings)'
    assert client_secret is not None, 'You must provide a ROGERTALK_CLIENT_SECRET in the settings passed into rogertalk.get_session(settings)'

    return Session(client_id=client_id,
                   client_secret=client_secret)


class RogerTalk(BaseApi):
    """
    Generic wrapper object, to access the complex underlying object
    """
    def __init__(self, settings):
        self.settings = settings
        self.session = get_session(self.settings)

    def stream(self, **kwargs):
        return Stream(session=self.session,
                      **kwargs)
