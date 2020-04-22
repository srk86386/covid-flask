from tweet_harvester import app
from flaskwebgui import FlaskUI #get the FlaskUI class
#from webui import WebUI # Add WebUI to your imports
# 'app' originates from the line 'app = Flask(__name__)'
# Feed it the flask app instance

##ui = WebUI(app, debug=True) # Create a WebUI instance
ui = FlaskUI(app)
ui.run()
#app.run(port=8080)
