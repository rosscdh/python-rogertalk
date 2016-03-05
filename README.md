python-rogertalk
=============

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
# DEBUG = True            ## Means a Development Session
# SECUPAY_DEBUG = True    ## Means demo = 1 sent to secupay regardless of environment
# SECUPAY_TOKEN = '<string api from the secupay website>'
#
from django.conf import settings
from secupay import RogerTalk

sp = RogerTalk(settings=settings)
```


## Tests

We use py.test

```
py.test -vvv```


ToDo
----

1. Integrate with requests-oauth2
3. Tests
