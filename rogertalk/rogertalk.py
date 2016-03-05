# -*- coding: UTF-8 -*-
import re
import json
import requests
import urlparse

import logging
logger = logging.getLogger('rogertalk')

SUPPORTED_LANGUAGES = (
    ('de_DE', 'Deutsch'),
    ('en_US', 'English')
)


class BadApiServesHTMLInsteadOfJsonExcepton(Exception):
    message = 'This api, is misconfigured. It serves HTML instead of a valid api format (json) as a response'


class InvalidApiResponse(Exception): pass


class Session(object):
    """
    Session object
    """
    site = 'https://api.rogertalk.com/'
    token = None

    def __init__(self, token, **kwargs):
        self.token = token
        # We default to english as translation should be the responsibility
        # of the implementing client, not the provider
        self.language = kwargs.pop('language', 'en_US')
        self.is_development = kwargs.pop('is_development', True)
        self.is_demo = kwargs.pop('is_demo', True)
        self.labels = kwargs.pop('ROGERTALK_LABELS', None)


class BaseApi(object):
    r = requests
    http_methods_allowed = ['get', 'post', 'patch', 'put', 'delete']

    def __init__(self, session, **kwargs):
        self.session = session
        self.token = session.token
        self.response = self.response_json = {}
        self.params = kwargs

    @property
    def base_url(self):
        return self.session.site

    @property
    def status_code(self):
        return getattr(self.response, 'status_code', None)

    @property
    def ok(self):
        return getattr(self.response, 'ok', None)

    @property
    def parse_uri(self):
        uri = self.uri

        for k, v in self.params.iteritems():
            key = ':{key}'.format(key=k)
            uri = uri.replace(key, str(v))

        return re.sub(r'\/\:(\w)+', '', uri)

    def headers(self, **kwargs):
        # We ONLY talk json, XML is very 1995 ;)
        headers = {
            'Content-Type': 'application/json; charset=utf-8;',
            'Accept': 'application/json;'
        }
        headers.update(kwargs)
        return headers

    def wrap_namespace(self, **kwargs):
        """
        Wrap all posted data in the structure that RogerTalk expects
        A flat dict with all the attributes just kinda mixed in there
        """
        kwargs.update({
            'apikey': self.token,
            'demo': self.session.is_demo.real  # Convert bool to 0 or 1 for php api
        })
        return json.dumps({'data': kwargs})

    def endpoint(self, *args, **kwargs):
        return urlparse.urljoin(self.base_url, self.parse_uri, *args, **kwargs)

    def process(self, response):
        self.response = response

        if response.ok is True:

            try:
                self.response_json = self.response.json()
                return self.response_json

            except ValueError as e:
                if e.message == 'No JSON object could be decoded':
                    raise BadApiServesHTMLInsteadOfJsonExcepton(e.message)
                else:
                    raise InvalidApiResponse(e.message)

        #
        # Handle the bad CLI api implementation of 404 returning HTML and not
        # a valid REST reponse
        #
        raise InvalidApiResponse('Secupay Api returned (%s) an invalid response: %s %s' % (response.status_code, response.url, response.content))

    def get(self, **kwargs):
        if 'get' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.get(self.endpoint(),
                            headers=self.headers(),
                            params=kwargs))

    def post(self, **kwargs):
        if 'post' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.post(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def put(self, **kwargs):
        if 'put' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.put(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def patch(self, **kwargs):
        if 'patch' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.patch(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def delete(self, **kwargs):
        if 'delete' not in self.http_methods_allowed:
            raise Exception('Method not allowed')

        return self.process(response=self.r.delete(self.endpoint(),
                            headers=self.headers(),
                            params=kwargs))


class Stream(BaseApi):
    uri = 'streams/:stream_id'
    http_methods_allowed = ['get', 'post']
    stream_id = None
    _data = {}

    def __init__(self, **kwargs):
        self.stream_id = kwargs.pop('stream_id', None)
        super(Stream, self).__init__(**kwargs)

    class Image(BaseApi):
        uri = 'image'
        http_methods_allowed = ['delete']

    class Participants(BaseApi):
        uri = 'participants'
        http_methods_allowed = ['delete', 'post']

    class Chunks(BaseApi):
        uri = 'chunks'
        http_methods_allowed = ['get', 'post']

    def image(self, **kwargs):
        return self.Image(session=self.session)

    def participants(self, **kwargs):
        return self.Participants(session=self.session)

    def chunks(self, **kwargs):
        return self.Chunks(session=self.session)
