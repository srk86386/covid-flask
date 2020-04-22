from flask import Flask, json, request,url_for
import tweepy
from flask import render_template

import os
from random import choice
from pymongo import MongoClient


# connect
client = MongoClient()
#db.profiles.create_index([('twt_id', pymongo.ASCENDING)],unique=True)
db = client.tweeter_db
collection = db.news_tweets
updates_coll = db.updates


app = Flask(__name__)
# Load our config from an object, or module (config.py)
app.config.from_object('config')

# These config variables come from 'config.py'
auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                           app.config['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
                      app.config['TWITTER_ACCESS_TOKEN_SECRET'])
tweepy_api = tweepy.API(auth)


@app.route('/tweet-harvester/wc')
def get_all_images():
    #import glob
    #path = 'c:\\projects\\hc2\\'
    #names= []
    #names.clear()
    names = os.listdir(os.path.join(app.static_folder, 'images'))
    #img_url = url_for('static', filename=os.path.join('images', choice(names)))
    #files = request.files.getlist("files[]")
    #files = request.files['images']
    #print(names)
    #print(img_url)
    return render_template("show_pics.html",files=names)

def get_data_for_index():
    #updates=list(client.covid_db.raw_data.find({'dateannounced':{'$ne':''}}).limit(10))
    updates = list(client.covid_db.raw_data.find({'$and':[{'dateannounced':{'$ne':''}},{'patientnumber':{'$ne':''}}]},{'_id':0}).limit(100))
    return updates

@app.route('/')
def index_page():
    #list(db.rawPatientData.find({},{'_id':0}).limit(3))
    return render_template("index.html", data=get_data_for_index())

def query_tweets(query= 'None'):
    all_channels = list(updates_coll.distinct('u_screen_name'))
    if query == 'None':
        tweets = list(updates_coll.find().sort('twt_id',-1))
        return [all_channels,tweets]
    else:
        tweets = list(updates_coll.find({'u_screen_name':query}).sort('twt_id',-1))
        return [all_channels,tweets]

# @app.route('/tweet-harvester/<string:username>')
# def user_tweets(username):
#   # 'tweets' is passed as a keyword-arg (**kwargs)
#   # **kwargs are bound to the 'tweets.html' Jinja Template context
#   return render_template("tweets.html", tweets=get_tweets(username))

@app.route('/tweet-harvester/<string:query>')
def tweets(query):
    # 'tweets' is passed as a keyword-arg (**kwargs)
    # **kwargs are bound to the 'tweets.html' Jinja Template context
    return render_template("tweets.html", tweets=query_tweets(query))
#
# @app.route('/tweet-harvester/<string:query>')
# def query_tweets():
#     # 'tweets' is passed as a keyword-arg (**kwargs)
#     # **kwargs are bound to the 'tweets.html' Jinja Template context
#     return render_template("tweets.html", tweets=query_tweets(query))
