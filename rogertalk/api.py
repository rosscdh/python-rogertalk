# -*- coding: UTF-8 -*-
import logging
logger = logging.getLogger('rogertalk')

from rogertalk.core import BaseApi
from rogertalk.validators import require_stream_id


class Stream(BaseApi):
    uri = '/streams/:stream_id'
    http_methods_allowed = ['get', 'post']
    stream_id = None
    _data = {}

    def __init__(self, **kwargs):
        self.stream_id = kwargs.get('stream_id', None)
        super(Stream, self).__init__(**kwargs)

    class Image(BaseApi):
        """
        Sub Class deals with a streams Image
        """
        uri = '/image'
        http_methods_allowed = ['delete']
        validators = [require_stream_id]

    class Participants(BaseApi):
        """
        Sub Class deals with a streams Participants
        """
        uri = '/participants'
        http_methods_allowed = ['delete', 'post']
        validators = [require_stream_id]

    class Chunks(BaseApi):
        """
        Sub Class deals with a streams Audio Chunks
        """
        uri = '/chunks'
        http_methods_allowed = ['get', 'post']
        validators = [require_stream_id]

    def my(self):
        return self.session.profile.get('streams')

    def image(self, **kwargs):
        return self.Image(session=self.session)

    def participants(self, **kwargs):
        return self.Participants(session=self.session)

    def chunks(self, **kwargs):
        return self.Chunks(session=self.session)
