from .tweets import *
from .database import *

from kkfw.celery import app


def joinRequest(screen_name):
    chain = getFriendshipWithMe.s(screen_name) | joinRequestFriendsInfo.s(screen_name)
    chain()

@app.task
def joinRequestFriendsInfo(info, screen_name):
    if not info['following']:
        update_status_template('follow-me-please.txt', screen_name)
    elif not info['followed_by']:
        chain = create_friendship.s(screen_name) | getFriendshipWithMe.s(screen_name) | joinFollowedBack.s(screen_name)
        chain()
    else:
        # ok - We been followed and followed_back ok
        # Might be a mutliple join or testing
        chain = joinFollowedBack.s(info, screen_name)
        chain()

@app.task
def joinFollowedBack(info, screen_name):
    if not info['followed_by']:
        update_status_template('must-allow-follow.txt', screen_name)
    else:
        # ok - We been followed and followed_back ok
        # But does player already exists and maybe on holiday
        epnoh = existsPlayerNotOnHoliday(screen_name)
        if epnoh is None:
            # Add to database and announce sucess - via tweet
            insertPlayer(screen_name)
            dm_template('joined-welcome.txt', screen_name)
        elif not epnoh:
            # Player exists and not on holiday
            dm_template('joined-already.txt', screen_name)
        elif epnoh:
            dm_template('joined-on-holiday.txt', screen_name)

def leaveRequest(screen_name):
    pass
