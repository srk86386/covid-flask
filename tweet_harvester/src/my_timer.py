import threading
import tweeter_user as twt
import get_json_data as json_data
import create_word_clouds as wc
import summary_image as summary
import graphwiz as graphs
import Pasta_graph as extra_graphs
def do_something():
  print("initiating get methodes..")
  print("getting data from tweeter for news channels.")
  twt.main_entry()
  print("getting the json data from api for the patients.")
  json_data.get_data()
  print("creating word cloud.")
  wc.interval()
  wc.key_word_cloud()

  print("creating graphs")
  graphs.controller()

  extra_graphs.main_entry()

  print("creating summary image")
  summary.create_summery()



def printit():
  thirty_mins = 30*60
  threading.Timer(thirty_mins, printit).start()
  print("Hello, World!")
  do_something()

printit()


input()
