from __future__ import absolute_import
from kkfw.celery import app
from kkfw.credentialsreply import *
from kkfw.templates import env

import tweepy
import time

def returnAPI():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.secure = True
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

@app.task(rate_limit='100/h')
def update_status(text):
    api = returnAPI()    
    api.update_status(text=text)

@app.task(rate_limit='1000/h') # reduce to 100
def dummy_update_status(text):
    print("Dummy :", text) 

@app.task(rate_limit='400/h') # reduce to 40
def dm(screen_name, text):
    api = returnAPI()    
    api.send_direct_message(screen_name=screen_name, text=text)

@app.task(rate_limit='400/h') # reduce to 40
def dummy_dm(screen_name, text):
    print("Dummy :", screen_name, " dmed", text) 

@app.task(rate_limit='40/h')
def create_friendship(screen_name):
    api = returnAPI()    
    api.create_friendship(screen_name=screen_name)

@app.task(rate_limit='400/h')  # reduce to 40
def getFriendshipWithMe(screen_name):
    api = returnAPI()    
    friendships = api.show_friendship(source_screen_name=screen_name,
                                     target_screen_name=SCREEN_NAME)
    info = {
         'following': friendships[0].following, 
         'followed_by': friendships[0].followed_by
         }
    return info

def update_status_template(template, screen_name):
    text =  env.get_template(template).render(screen_name=screen_name)
    dummy_update_status.delay(text)

def dm_template(template, screen_name):
    text =  env.get_template(template).render(screen_name=screen_name)
    dummy_dm.delay(screen_name, text)
