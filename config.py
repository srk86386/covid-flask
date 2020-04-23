import os
import urllib
#DEBUG = True
# Enable stacktrace & debugger in web browser
TWITTER_CONSUMER_KEY = 'NUIKNlSijJbNf8c8DC7IEzxBu'
TWITTER_CONSUMER_SECRET = 'sqdWyzQhyXYAnXgLWa8BbERNODBcTRPZLCDW4JCGdS8BKyrsTO'
TWITTER_ACCESS_TOKEN = '717406917237157888-UCExysj6JGBSHuEGu6RI2uVp5R7hSOn'
TWITTER_ACCESS_TOKEN_SECRET = 'ikDMNbGWbeoFAsolgj7nGBg6BH0EkAjYgw4kCYzR2JmK3'

username = urllib.parse.quote_plus('rahul')
password = urllib.parse.quote_plus('qwert@12')
MONGO_DB_URI = f"mongodb+srv://{username}:{password}@covid0-oir2o.mongodb.net/test?retryWrites=true&w=majority"
TEMPLATES_AUTO_RELOAD = True
