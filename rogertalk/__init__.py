# -*- coding: UTF-8 -*-
from .rogertalk import DevelopmentSession, Session
from .rogertalk import BaseApi, Payment, PaymentTypes
from .utils import get_namedtuple_choices


def get_session(settings):
    if type(settings) is dict:
        is_development = settings.get('ROGERTALK_DEVELOPMENT', True)
        is_demo = settings.get('ROGERTALK_DEMO', True)
        language = settings.get('ROGERTALK_LANGUAGE', 'en_US')
        token = settings.get('ROGERTALK_TOKEN', None)
    else:
        is_development = getattr(settings, 'ROGERTALK_DEVELOPMENT', True)
        is_demo = getattr(settings, 'ROGERTALK_DEMO', True)
        language = getattr(settings, 'ROGERTALK_LANGUAGE', 'en_US')
        token = getattr(settings, 'ROGERTALK_TOKEN', None)

    ROGERTALK_LABELS = getattr(settings, 'ROGERTALK_LABELS', {
        "en_US": {
            "basket_title": "Your Order",
            "submit_button_title": "Submit",
            "cancel_button_title": "Return to Basket"
        },
        "de_DE": {
            "basket_title": "Ihre Bestellung",
            "submit_button_title": "Daten Ubermitteln",
            "cancel_button_title": "Zum Warenkorb"
        }
    })

    assert token is not None, 'You must provide a ROGERTALK_TOKEN in the settings passed into rogertalk.get_session(settings)'

    if is_development is False:

        return Session(token=token,
                       is_development=False,
                       is_demo=is_demo,
                       language=language,
                       ROGERTALK_LABELS=ROGERTALK_LABELS)

    return DevelopmentSession(token=token,
                              is_development=True,
                              is_demo=is_demo,
                              language=language,
                              ROGERTALK_LABELS=ROGERTALK_LABELS)


class RogerTalk(BaseApi):
    """
    Generic wrapper object, to access the complex underlying object
    """
    def __init__(self, settings):
        self.settings = settings
        self.session = get_session(self.settings)
