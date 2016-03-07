python-rogertalk
================

(in-development) Python Client for rogertalk.com


Installation
------------

```
git clone https://github.com/rosscdh/python-rogertalk.git
cd python-rogertalk
python setup.py install
```


## Basic Usage

```
#
# settings should be a dict object or have an implementation of
# getattr and provide the following
#
#
from rogertalk import RogerTalk

DEV_SETTINGS = {
    'ROGERTALK_CLIENT_ID': ':client_id',
    'ROGERTALK_CLIENT_SECRET': ':client_secret',
}

rogerroger = RogerTalk(settings=DEV_SETTINGS)
rogerroger.stream(stream_id=261360002).get()
```

** Result **

```
{u'total_duration': 14367, u'color': None, u'created': 1457211062009, u'joined': 1457211062009, u'last_played_from': 1457211062009, u'played_until': 1457211062009, u'visible': True, u'image_url': None, u'others_listened': 1457211062009, u'last_interaction': 1457211062618, u'others': [{u'username': u'rogerbot', u'display_name': u'Rogerbot', u'image_url': u'https://api.rogertalk.com/file/b55eedb9daa758bcbee306767d6c6df62a037c673688c02bcf655a00f3007a46-p.jpg', u'location': u'New York', u'active': True, u'timezone': u'America/New_York', u'id': 6410001}], u'chunks': [{u'end': 1457211062618, u'audio_url': u'https://api.rogertalk.com/file/cfc21ccf7045f15aac5c2db0f82029d5f9f49b38a5e4f9a501d9e97bca4d961a-p.mp3', u'sender_id': 6410001, u'start': 1457211048251, u'duration': 14367, u'id': 1}], u'title': None, u'id': 261360002}

```

### My Streams ###

```
rogerroger.stream().my()

[{u'total_duration': 14367, u'color': None, u'created': 1457211062009, u'joined': 1457211062009, u'last_played_from': 1457211062009, u'played_until': 1457211062009, u'visible': True, u'image_url': None, u'others_listened': 1457211062009, u'last_interaction': 1457211062618, u'others': [{u'username': u'rogerbot', u'display_name': u'Rogerbot', u'image_url': u'https://api.rogertalk.com/file/b55eedb9daa758bcbee306767d6c6df62a037c673688c02bcf655a00f3007a46-p.jpg', u'location': u'New York', u'active': True, u'timezone': u'America/New_York', u'id': 6410001}], u'chunks': [{u'end': 1457211062618, u'audio_url': u'https://api.rogertalk.com/file/cfc21ccf7045f15aac5c2db0f82029d5f9f49b38a5e4f9a501d9e97bca4d961a-p.mp3', u'sender_id': 6410001, u'start': 1457211048251, u'duration': 14367, u'id': 1}], u'title': None, u'id': 261360002}]
```


## Tests

We use py.test

```
py.test -vvv```


ToDo
----

1. ~~Integrate with requests-oauth2~~ **not necessary** oauth2 lib is implemented with grant_type password
3. Tests
