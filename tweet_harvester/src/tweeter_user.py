import tweepy #https://github.com/tweepy/tweepy
import csv
import pandas as pd
from pymongo import MongoClient
import pymongo
import time
import re
import os
import pytz
import datetime


wd = os.getcwd()

#print(wd)

client = MongoClient()
#db.profiles.create_index([('twt_id', pymongo.ASCENDING)],unique=True)
db = client.tweeter_db
collection = db.news_tweets
updates_coll = db.updates
updates_coll.remove({});

auth_vars = []
f = open("auth", "r")
for line in f:
    #print(line.strip())
    auth_vars.append(line.strip())
f.close()

#print(auth_vars)

#Twitter API credentials
consumer_key = auth_vars[0]
consumer_secret = auth_vars[1]
access_key = auth_vars[2]
access_secret = auth_vars[3]

#print(consumer_key)

def convert_datetime_timezone(dt, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    dt = datetime.datetime.strptime(dt,"%a %b %d %H:%M:%S +0000 %Y")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%a, %d %b %Y %I:%M:%S %p")

    return dt


def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())


def save_tweets(alltweets):
     for tweet in alltweets:
        #to parse tweeter status object and geeting only json object of tweet
        try:
            tweet = tweet._json
            #print("done json parsing")
        except:
            #print("error in json parsing")
            pass
        tweet_id = tweet["id"]
        created = tweet["created_at"]
        entities= tweet['entities']
        favorite_count = tweet['favorite_count']
        in_reply_to_screen_name = tweet['in_reply_to_screen_name']
        tweet_text = str(tweet["text"])
        cleaned = clean_tweet(tweet_text)
        tweet_src = str(tweet["source"])
        screen_name = str(tweet["user"]['screen_name'])
        u_name = str(tweet["user"]['name'])
        u_id = str(tweet["user"]['id'])
        u_url = tweet['user']['url']
        followers_count = str(tweet["user"]['followers_count'])
        user_friends = str(tweet["user"]['friends_count'])
        lang = str(tweet["lang"])
        place = str(tweet["place"])
        locasn = str(tweet['user']['location'])
        local_time = convert_datetime_timezone(created, "GMT", "Asia/Calcutta")
        timestamp = datetime.datetime.strptime(local_time, '%a, %d %b %Y %I:%M:%S %p').strftime('%Y%m%d%H%M%S') #converting time in YYYYMMDDHHMMSS
        #tweetslist.append([tweet_id, created, tweet_text,tweet_src, screen_name,u_name,u_id,followers_count,user_friends,lang,place,locasn])
        #print(tweet)
        tweet_to_save=({'twt_id':tweet_id, 'created_at':created, 'entities':entities, 'favorite_count': favorite_count,
                       'in_reply_to_screen_name': in_reply_to_screen_name, 'text':tweet_text, 'cleaned_text':cleaned,
                      'source':tweet_src, 'u_screen_name':screen_name, 'u_name':u_name,'u_id':u_id, 'u_followers_count':followers_count,
                       'u_url':u_url, 'friends_count':user_friends, 'lang':lang,'place':place,'u_location':locasn, 'created_at_ist':local_time,
                       'timestamp_ist':int(time.time()), 'tmstamp':timestamp
            })
        try:
            collection.insert_one(tweet_to_save)
            updates_coll.insert_one({'twt_id':tweet_id, 'created_at':created, 'text':tweet_text, 'cleaned_text':cleaned,
                                    'u_screen_name':screen_name, 'u_url':u_url, 'created_at_ist':local_time})
        except Exception as e:
            print(e)
        #print('inserted')

    #cols = ['tweet_id', 'created_at','tweet_text','tweet_source','user_screen_name', 'user_name','user_id', 'user_followers_count',
            #'user_friends_count','tweet_lang', 'user_place', 'user_location']
    #df = pd.DataFrame(tweetslist, columns = cols)
    #df.to_csv(screen_name+'tweets.csv')

def get_all_tweets(profile_name,last_tweet):

    get_tweets=True

    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    tweetslist =[]


    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = profile_name,count=100)

    for tweet in new_tweets:
        #tweet = tweet._json
        if last_tweet == tweet.id:
            #print(f"got the last tweet ID {last_tweet, tweet.id}")
            get_tweets=False
            break
        else:
            alltweets.append(tweet)
            #get_tweets==True
    #save most recent tweets
    #alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    try:
        # try to get the letest update from twitter,
        #if there is no update the alltweets wont have any item and hence fail with index error
        oldest = alltweets[-1].id - 1
    except:
        return

    #keep grabbing tweets until there are no tweets left to grab
    while (len(new_tweets) > 0) and get_tweets==True:
        print("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = profile_name,count=200,max_id=oldest)

        for tweet in new_tweets:
            #tweet = tweet._json
            if last_tweet == tweet.id:
                #print(f"got the last tweet ID {last_tweet, tweet.id}")
                get_tweets=False
                break
            else:
                alltweets.append(tweet)

        #save most recent tweets
        #alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print (f"...{len(alltweets)} tweets downloaded so far for {profile_name}")
    print (f"...{len(alltweets)} tweets downloaded for {profile_name}")
    save_tweets(alltweets)
    #cols = ['tweet_id', 'created_at','tweet_text','tweet_source','user_screen_name', 'user_name','user_id',
    #'user_followers_count', 'user_friends_count','tweet_lang', 'user_place', 'user_location']
    #df = pd.DataFrame(tweetslist, columns = cols)
    #df.to_csv(screen_name+'tweets.csv')

def main_entry(all_channels=['timesofindia','ndtv','TimesNow','aajtak','ABPNews','EconomicTimes','htTweets','PTI_News','ANI']):
    for channel in all_channels:
        try:
            #dttm = collection.find_one({'user.screen_name':'timesofindia'},{'created_at':1,'_id':0})['created_at']
            #last_updated = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(dttm,'%a %b %d %H:%M:%S +0000 %Y'))
            all_col = collection.find({'u_screen_name':channel},{'twt_id':1,'_id':0}).sort('twt_id', pymongo.DESCENDING)
            last_tweet = all_col[0]['twt_id']
        except:
            last_tweet='null'

        print(channel, last_tweet)
        #time.sleep(10)
        get_all_tweets(channel, last_tweet)
#import sleep
if __name__ == '__main__':
    #pass in the username of the account you want to download
    #ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime('Tue Mar 31 21:30:00 +0000 2020','%a %b %d %H:%M:%S +0000 %Y'))
    main_entry()
else:
    pass
