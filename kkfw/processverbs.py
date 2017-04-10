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
        chain = joinFollowedBack.s(info, screen_name=screen_name)
        chain()

@app.task
def joinFollowedBack(info, screen_name):
    if not info['followed_by']:
        update_status_template('must-allow-follow.txt', screen_name=screen_name)
    else:
        # ok - We been followed and followed_back ok
        # But does player already exists and maybe on holiday
        epnoh = existsPlayerNotOnHoliday(screen_name=screen_name)
        if epnoh is None:
            # Add to database and announce sucess - via tweet
            insertPlayer(screen_name)
            dm_template('joined-welcome.txt', screen_name=screen_name)
        elif not epnoh:
            # Player exists and not on holiday
            dm_template('joined-already.txt', screen_name=screen_name)
        elif epnoh:
            restorePlayer(screen_name)
            dm_template('joined-on-holiday.txt', screen_name=screen_name)

def leaveRequest(screen_name):
    removePlayer(screen_name)
    destroy_friendship.delay(screen_name)
    update_status_template('leaving.txt', screen_name=screen_name)

def holidayRequest(screen_name):
    removePlayer(screen_name)
    update_status_template('holiday.txt', screen_name=screen_name)

def newsSeriesRequest(screen_name, silly_name):
    if(isAdmin(screen_name)):
        seriesID = newSeries(silly_name)
        newRoundRequest(screen_name)

def newRoundRequest(screen_name):
    if(isAdmin(screen_name)):
        r = newRound()
        dm_template('new-round.txt', screen_name, 
                    silly_name=r['silly_name'], 
                    entry_by=r['entry_by'],
                    gamed_played_by=r['gamed_played_by'])
