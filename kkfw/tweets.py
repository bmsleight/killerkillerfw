from __future__ import absolute_import
from kkfw.celery import app
from kkfw.credentialsreply import *

import tweepy
import time

def returnAPI():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.secure = True
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def dmRateLimited(screen_name, text):
    r = dm.delay(screen_name, text)

@app.task
def dm(screen_name, text):
    api = returnAPI()    
    api.send_direct_message(screen_name=screen_name, text=text)

