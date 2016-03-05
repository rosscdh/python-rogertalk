# -*- coding: UTF-8 -*-
import json
import pytest
import httpretty

from rogertalk import RogerTalk

DEV_SETTINGS = {
    'ROGERTALK_DEVELOPMENT': True,
    'ROGERTALK_DEMO': True,
    'ROGERTALK_TOKEN': '12345',
}

subject = RogerTalk(settings=DEV_SETTINGS)


@httpretty.activate
def test_payment_types():
    expected_response = {
                          "status": "ok",
                          "errors": None,
                          "data": [
                            "debit",
                            "creditcard",
                            "prepay",
                            "invoice",
                            "subscription"
                          ]
                        }

    httpretty.register_uri(httpretty.POST, "https://api.rogertalk.com/payment/gettypes",
                           body=json.dumps(expected_response),
                           content_type="application/json")
    response = subject.payment_types()
    assert response == expected_response

def test_invalid_payment_types_request():
    # Must not allow get requests
    with pytest.raises(Exception):
        subject.payment_types().get()


def test_payment():
    assert subject.payment().__class__.__name__ == 'Payment'
    assert subject.payment().uri == 'payment/init'


@httpretty.activate
def test_make_payment():
    expected_response = {
        "status": "ok",
        "data": {
            "hash": "tujevzgobryk3303",
            "iframe_url": "https://api.rogertalk.ag/payment/tujevzgobryk3303"
        },
        "errors": None
    }
    httpretty.register_uri(httpretty.POST, "https://api.rogertalk.com/payment/init",
                           body=json.dumps(expected_response),
                           content_type="application/json")

    payment = subject.payment()

    response = payment.make_payment(amount=25.00,
                                    payment_type='debit',
                                    url_success='http://localhost/payment/success/',
                                    url_failure='http://localhost/payment/fail/',
                                    url_push='http://localhost/payment/status/')

    assert response == expected_response

    expected_posted_data = {'amount': 2500,
                            'labels': {'de_DE': {'basket_title': 'Ihre Bestellung',
                                                 'cancel_button_title': 'Zum Warenkorb',
                                                 'submit_button_title': 'Daten Ubermitteln'},
                                       'en_US': {'basket_title': 'Your Order',
                                                 'cancel_button_title': 'Return to Basket',
                                                 'submit_button_title': 'Submit'}},
                            'payment_type': 'debit',
                            'url_failure': 'http://localhost/payment/fail/',
                            'url_push': 'http://localhost/payment/status/',
                            'url_success': 'http://localhost/payment/success/'}

    assert payment.send_data == expected_posted_data


@httpretty.activate
def test_payment_capture_preauthorized_payment():
    expected_response = {
        "status": "ok",
        "data": {
            "status": "ok",
        },
        "errors": None
    }
    httpretty.register_uri(httpretty.POST, "https://api.rogertalk.com/payment/tujevzgobryk3303/capture",
                           body=json.dumps(expected_response),
                           content_type="application/json")

    response = subject.payment().capture_preauthorized_payment(token='tujevzgobryk3303')
    assert response == expected_response

@httpretty.activate
def test_payment_cancel_preauthorized_payment():
    expected_response = {
        "status": "ok",
        "data": {
            "status": "ok",
        },
        "errors": None
    }
    httpretty.register_uri(httpretty.POST, "https://api.rogertalk.com/payment/tujevzgobryk3303/cancel",
                           body=json.dumps(expected_response),
                           content_type="application/json")

    response = subject.payment().cancel_preauthorized_payment(token='tujevzgobryk3303')
    assert response == expected_response
