from .tweets import *
from kkfw.celery import app


def joinRequest(screen_name):
    #add.apply_async((2, 2), link=other_task.s())
#    friendship = getFriendshipWithMe.apply_async(screen_name, 
#                                               link=joinRequestFriendsInfo(screen_name, "n") )
#    f = getFriendshipWithMe.delay(screen_name)
#    friendships = f.get()
#    print(friendships[0].following, screen_name)

    chain = getFriendshipWithMe.s(screen_name) | joinRequestFriendsInfo.s(screen_name)
    chain()

@app.task
def joinRequestFriendsInfo(screen_name, info):
    print(screen_name, info)

def leaveRequest(screen_name):
    pass
