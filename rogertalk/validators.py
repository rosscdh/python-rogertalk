# -*- coding: UTF-8 -*-
import logging
logger = logging.getLogger('rogertalk')


class ValidationError(Exception):
    pass


def require_stream_id(**kwargs):
    if 'stream_id' not in kwargs.keys():
        raise ValidationError('stream_id must be provided')

    stream_id = kwargs.get('stream_id')

    if type(stream_id) is not int:
        raise ValidationError('stream_id must be an Integer')
