from pymongo import MongoClient
import time
import urllib
username = urllib.parse.quote_plus('rahul')
password = urllib.parse.quote_plus('qwert@12')
MONGO_DB_URI = f"mongodb+srv://{username}:{password}@covid0-oir2o.mongodb.net/test?retryWrites=true&w=majority"

def connect():
    client = MongoClient(MONGO_DB_URI)
    #db = client.tweeter_db
    return client
