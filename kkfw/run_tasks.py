from .tasks import *

import tweepy, json, time
from kkfw.credentials import *

def putTwiiterStreamMessageToServer(user_id, screen_name, text, me):
    print(user_id, screen_name, text, me)
    if screen_name != me:
        processInComing.delay(user_id, screen_name, text)

class StdOutListener( tweepy.StreamListener ):
    def __init__( self, me ):
        self.tweetCount = 0
        self.me = me
        print("I am ", me)
    def on_connect( self ):
        print("Connection established!!")
    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)
    def on_data( self, status ):
        # print("Entered on_data()")
        d = json.loads(status)
        for key in d.keys():
            if key == 'direct_message':
                putTwiiterStreamMessageToServer(
                  d['direct_message']['sender_id_str'], 
                  d['direct_message']['sender_screen_name'], 
                  d['direct_message']['text'],
                  self.me)
            if key == 'text':
                putTwiiterStreamMessageToServer(
                  d['user']['id_str'], 
                  d['user']['screen_name'], 
                  d['text'].split(' ', 1)[1],
                  self.me)
        return True
    def on_error( self, status ):
        print(status)

def main():
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.secure = True
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
        print(api.me().screen_name)
        stream = tweepy.Stream(auth, StdOutListener(me=api.me().screen_name))
        stream.userstream()
    except (KeyboardInterrupt, SystemExit):
        print("Keyboard")
        quit(0)
    except BaseException as e:
        print("Error in main()", e)
        time.sleep(10)
    finally:
        pass

if __name__ == '__main__':
    main()
