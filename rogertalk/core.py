# -*- coding: UTF-8 -*-
import re
import json
import requests
import urlparse
from dotmap import DotMap

import logging
logger = logging.getLogger('rogertalk')

#
# Exceptions
#
class MethodNotAllowedError(Exception): pass
class InvalidApiResponse(Exception): pass
class AuthenticationError(Exception): pass


#
# Decorators
#
def validate(view_func):
    """
    Decorator that executes validation schems against the passed in params
    """
    def func_wrapper(self, *args, **kwargs):
        print args
        for validator in self.validators:
            print validator
        return view_func(self)
    return func_wrapper


#
# Session object
# Logs user in and stores the response as profile and access_token
#
class Session(object):
    """
    Session object
    """
    site = 'https://api.rogertalk.com'
    version = 'v10'
    access_token = None
    refresh_token = None
    version = 10
    session = None
    profile = None

    def __init__(self, client_id, client_secret, **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret
        try:
            self.session = self.login()
        except Exception as e:
            raise AuthenticationError(e.message)

        self.profile = DotMap(self.session.json())
        self.access_token = self.profile.access_token
        self.refresh_token = self.profile.refresh_token

    def login(self):
        url = '{base_url}/oauth2/token?api_version={version}&grant_type=password&username={username}&client_id={client_id}'.format(base_url=self.site,
                                                                                                                                   version=self.version,
                                                                                                                                   username=self.client_id,
                                                                                                                                   client_id='aberacadabera')
        resp = requests.post(url, data={'password': self.client_secret})

        if resp.ok is True:
            return resp
        else:
            raise AuthenticationError(resp.content)


#
# Base Api Object
#

class BaseApi(object):
    """
    Api Client Objects, wrapper for functionality
    """
    r = requests
    http_methods_allowed = ['get', 'post', 'patch', 'put', 'delete']
    validators = []

    def __init__(self, session, **kwargs):
        self.session = session
        self.access_token = session.access_token
        self.refresh_token = session.refresh_token
        self.response = self.response_json = {}
        self.params = kwargs

    def _method_is_allowed(self, method):
        if method not in self.http_methods_allowed:
            raise MethodNotAllowedError('Method not allowed')

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
            'Authorization': 'Bearer {access_token}'.format(access_token=self.access_token),
            'Content-Type': 'application/json; charset=utf-8;',
            'Accept': 'application/json;'
        }
        headers.update(kwargs)
        return headers

    @validate
    def wrap_namespace(self, **kwargs):
        """
        Wrap all posted data in the structure that RogerTalk expects
        A flat dict with all the attributes just kinda mixed in there
        """
        kwargs.update({})
        return json.dumps({'data': kwargs})

    def endpoint(self, *args, **kwargs):
        uri_path = '/v{version}{uri}'.format(version=self.session.version, uri=self.parse_uri)
        return urlparse.urljoin(self.base_url, uri_path, *args, **kwargs)

    def process(self, response):
        self.response = response

        if response.ok is True:

            self.response_json = DotMap(self.response.json())
            return self.response_json

        #
        # Handle the bad CLI api implementation of 404 returning HTML and not
        # a valid REST reponse
        #
        raise InvalidApiResponse('Rogertalk Api returned (%s) an invalid response: %s %s' % (response.status_code, response.url, response.content))

    def get(self, **kwargs):
        self._method_is_allowed('get')
        return self.process(response=self.r.get(self.endpoint(),
                            headers=self.headers(),
                            params=kwargs))

    def post(self, **kwargs):
        self._method_is_allowed('post')
        return self.process(response=self.r.post(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def put(self, **kwargs):
        self._method_is_allowed('put')
        return self.process(response=self.r.put(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def patch(self, **kwargs):
        self._method_is_allowed('patch')
        return self.process(response=self.r.patch(self.endpoint(),
                            headers=self.headers(),
                            data=self.wrap_namespace(**kwargs)))

    def delete(self, **kwargs):
        self._method_is_allowed('delete')
        return self.process(response=self.r.delete(self.endpoint(),
                            headers=self.headers(),
                            params=kwargs))
