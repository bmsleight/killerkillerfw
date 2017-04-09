from __future__ import absolute_import
from kkfw.celery import app
from .tweets import *
from .helpers import *
from .processverbs import *


import time


@app.task
def processInComing(user_id, screen_name, text):
    r = ""
    #Split text into Verb and test of message
    (verb, rest_of_message) = verbSplit(text)

    if verb == 'JOIN':
        r = joinRequest(screen_name)
    if verb == 'LEAVE':
        r = leaveRequest(screen_name)
    
    return r

@app.task
def longtime_add(x, y):
    print('long time task begins')
    # sleep 5 seconds
    time.sleep(1)
    print('long time task finished')
    return x + y