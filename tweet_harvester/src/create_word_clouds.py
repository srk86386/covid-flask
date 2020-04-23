import matplotlib.pyplot as pPlot
from wordcloud import WordCloud, STOPWORDS
import numpy as npy
from PIL import Image
from pathlib import Path # to work with path
import base64
import db_utils


#from pymongo import MongoClient
#client = MongoClient()
#updates_coll = client.tweeter_db.updates
#main_col = client.tweeter_db.news_tweets

import time;
ts = time.time()

interval_file_name = str(int(ts))+".png"
img_dir = str(Path(__file__).parents[1])+"/static/images/"



def rm_stop_words(dataset):
    with open('stopwords.txt','r') as stop_words:
        words = stop_words.read()
        stop_words.close()

    stop_words = words.split(",")
    print(stop_words)
    dataset1 = ""

    dataset = dataset.replace("#","")
    for word in dataset.split(" "):
        if word in stop_words:
            pass
        else:
            dataset1 = dataset1+ " "+word
    return dataset1

def store_img_in_db(image_file):
    with open("test.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        #store str in mongo

def retrieve_img_from_db():
    with open("test2.jpg", "wb") as fimage:
        #read image in str and then convert it like this
        fimage.write(str.decode('base64'))


def create_word_cloud(data_string,img_file=interval_file_name):
   #maskArray = npy.array(Image.open("cloud.png"))
   #cloud = WordCloud(background_color = "white", max_words = 200, mask = maskArray, stopwords = set(STOPWORDS)) #with mask
   dataset = data_string.lower()

   #let us remove the stop words recognized by us
   dataset = rm_stop_words(dataset)

   cloud = WordCloud(background_color = "white", max_words = 200, stopwords = set(STOPWORDS))  #without mask
   cloud.generate(dataset)
   #img_file = "wc.png"    #hardcoding name for now
   cloud.to_file(img_dir+img_file)

def generic_wc():
    """ This is to practice and understand how the words cloud can be built"""
    # file name will be stored in interval_file_name
    pass

def interval():
    # file name will be stored in interval_file_name
    client = db_utils.connect()
    data = " ".join([item['cleaned_text'] for item in client.tweeter_db.updates.find({},{'cleaned_text':1,'_id':0})])
    create_word_cloud(data,"wc.png")
    """ We will be generating word cloud, after every iteration """

    pass

def key_word_cloud(keyword='lockdown'):
    """ We will be generating word cloud, on keyword basis """
    #get the current date in the formate toquery
    dat_for_filter = time.strftime("%Y%m%d")
    client = db_utils.connect()
    data = " ".join([item['cleaned_text'] for item in client.tweeter_db.news_tweets.find({'$and':[{'cleaned_text':{'$regex':keyword,'$options':'i'}},
                                                                    {'tmstamp':{'$regex':'^'+dat_for_filter+'.*'}}]},{'cleaned_text':1,'_id':0})])
    client = None
    #need to drop keywords which match lockdown
    data = data.lower().replace(keyword,"")
    create_word_cloud(data, keyword+dat_for_filter+".png")

    pass

def till_date_wc():
    """ We will be generating word cloud, for all the tweets till date"""
    pass

if __name__ == "__main__":
    interval()
    key_word_cloud()
