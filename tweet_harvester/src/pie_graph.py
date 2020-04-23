import matplotlib.pyplot as plt
import matplotlib
from statistics import mean
from pathlib import Path # to work with path
import numpy as np
import db_utils
img_dir = str(Path(__file__).parents[1])+"/static/images/"

import time
import os,sys
#from pymongo import MongoClient
#client = MongoClient()
#coln = client.covid_db.raw_data

t_date = time.strftime("%d/%m/%Y")
#t_date = "09/04/2020"
#print(client.list_database_names())
#print(coln.count())
#print(t_date)
 # to get hospitalized data of all the states for current date

font = {#'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

#fig = plt.figure(figsize=(30,18))

def pie_chart():

    agg4=[{'$match':{'$and':[{'dateannounced':t_date},  {'currentstatus':'Hospitalized'} ]}},
         {'$group': {'_id': '$detectedstate','count': { '$sum': 1 }}},
         { '$sort' : { 'count' : -1} }
        ]

    client=db_utils.connect()
    data_confirmed = list(client.covid_db.raw_data.aggregate(agg4))
    client=None

    if len(data_confirmed)==0:
         return ""

    x= [k['_id'] for k in data_confirmed]
    y=[k['count'] for k in data_confirmed]


    #plt
    #fig = plt.figure(figsize=(30,18))
    #ax1 = fig.add_axes([0,0,1,1])  #rect − A 4-length sequence of [left, bottom, width, height] quantities.
    fig, ax1 = plt.subplots(figsize=(30,18), subplot_kw=dict(aspect="equal"))
    ax1.axis('equal')
    states = x #['C', 'C++', 'Java', 'Python', 'PHP']
    counts = y #[23,17,35,29,12]
    states = [f"{x[i]} ({y[i]})" for i in range(len(x))]

    # explode 1st slice
    explode = [0]*(len(x)-1)
    explode.insert(0,0.1)
    explode = tuple(explode)

    wedges, texts, autotexts = ax1.pie(counts, explode=explode,labels = states,
                                        shadow=False, autopct='%1.2f%%',rotatelabels =True) #startangle=-40,wedgeprops=dict(width=0.5)
    ax1.set_title(f"Pie chart showing statewise infected counts for current date. The total patients count is {sum(counts)}")
    #ax1.text(3, 8, 'boxed italics text in data coords', style='italic', bbox = {'facecolor': 'red'})
    #ax1.annotate('annotate', xy = (2, 1), xytext = (3, 4),arrowprops = dict(facecolor = 'black', shrink = 0.05))
    ax1.legend(wedges, states,
         title=f"States ({sum(counts)})",
         loc="upper right",
         bbox_to_anchor=(0.6, 0.1, 0.5, 1))
    #plt.show()
    plt.setp(autotexts, size=14, weight="bold")
    plt.savefig(img_dir+"Confirmed_statewise.png", facecolor='w', edgecolor='w')

def pie_chart_all_data():

     agg4=[{'$match':{'$and':[{'dateannounced':{'$ne':''}},  {'currentstatus':'Hospitalized'} ]}},
         {'$group': {'_id': '$detectedstate','count': { '$sum': 1 }}},
         { '$sort' : { 'count' : -1} }
        ]

     client=db_utils.connect()
     data_statewise = list(client.covid_db.raw_data.aggregate(agg4))
     client=None

     x= [k['_id'] for k in data_statewise]
     y=[k['count'] for k in data_statewise]


     #plt
     #fig = plt.figure(figsize=(30,18))
     #ax1 = fig.add_axes([0,0,1,1])  #rect − A 4-length sequence of [left, bottom, width, height] quantities.
     fig, ax1 = plt.subplots(figsize=(30,18), subplot_kw=dict(aspect="equal"))
     ax1.axis('equal')
     states = x #['C', 'C++', 'Java', 'Python', 'PHP']
     counts = y #[23,17,35,29,12]
     states = [f"{x[i]} ({y[i]})" for i in range(len(x))]

     # explode 1st slice
     explode = [0]*(len(x)-1)
     explode.insert(0,0.1)
     explode = tuple(explode)

     wedges, texts, autotexts = ax1.pie(counts, explode=explode,labels = states,
                                        shadow=False, autopct='%1.2f%%',rotatelabels =True) #startangle=-40,wedgeprops=dict(width=0.5)
     #ax1.set_title(f"Pie chart showing statewise infected counts for current date. The total patients count is {sum(counts)}")
     #ax1.text(3, 8, 'boxed italics text in data coords', style='italic', bbox = {'facecolor': 'red'})
     #ax1.annotate('annotate', xy = (2, 1), xytext = (3, 4),arrowprops = dict(facecolor = 'black', shrink = 0.05))
     ax1.legend(wedges, states,
          title=f" States (counts - {sum(counts)})",
          loc="upper right",
          bbox_to_anchor=(0.6, 0.1, 0.5, 1))
     #plt.show()
     plt.setp(autotexts, size=14, weight="bold")
     plt.savefig(img_dir+"Confirmed_statewise_all.png", facecolor='w', edgecolor='w')

def statewise_bar_graph(data_confirmed):

     #fig, ax = plt.subplots(figsize=(30,18))
     fig = plt.figure(figsize=(30,18))
     ax = fig.add_axes([0,0,1,1])
     #create x and y for plotting
     x= [k['_id'] for k in data_confirmed]
     y=[k['count'] for k in data_confirmed]
     #print(len(data_confirmed), len(x),len(y))


     plt.plot(x,y, label="line graph", color='r')
     plt.bar(x,y, label="bar graph", color='c')
     plt.xlabel("date of the patients confirmation")
     plt.xlabel("number of the patients confirmed")
     plt.title(f"Confirmed ({sum(y)}) corona virus cases in India")
     plt.legend()
     #plt.gcf().autofmt_xdate()


     for idx in range(len(x)):
         plt.text(x[idx], y[idx], str(y[idx]))
     #plt.show()
     plt.savefig(img_dir+"Confirmed_statewise.png", facecolor='w', edgecolor='w',orientation='portrait')

     #pie_chart(x,y)

if __name__=="__main__":
    pie_chart()
    pie_chart_all_data()
