from tweet_harvester import app
from flaskwebgui import FlaskUI #get the FlaskUI class
# 'app' originates from the line 'app = Flask(__name__)'
# Feed it the flask app instance


ui = FlaskUI(app)
ui.run()
#app.run(port=8080)
