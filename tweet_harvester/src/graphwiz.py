import matplotlib.pyplot as plt
import matplotlib
from statistics import mean
from pathlib import Path # to work with path
img_dir = str(Path(__file__).parents[1])+"/static/images/"

import time

from pymongo import MongoClient
t_date = time.strftime("%d/%m/%Y")

def config():
    coln = MongoClient().covid_db.raw_data
    #coln = client.covid_db.rawPatientData
    font = {#'family' : 'normal',
            'weight' : 'bold',
            'size'   : 22}
    matplotlib.rc('font', **font)
    return coln

def deconfig():
    coln = None


def get_all_data(coln):
     agg1=[{'$match':{'$and':[{'dateannounced':{'$ne':""}},  {'currentstatus':'Hospitalized'} ]}}, # reportedOn, status
             {'$group': {'_id': '$dateannounced','count': { '$sum': 1 }}},
            { '$project': {
                'dateannounced':1,'count':1,
              'date': {'$dateFromString': {
                'dateString': '$_id',
                'format': "%d/%m/%Y"
              }
            }}},
             { '$sort' : { 'date' : 1} }
            ]
     data_confirmed = list(coln.aggregate(agg1))

     agg2=[{'$match':{'$and':[{'dateannounced':{'$ne':""}},  {'currentstatus':'Recovered'} ]}},
         {'$group': {'_id': '$dateannounced','count': { '$sum': 1 }}},
        { '$project': {
            'dateannounced':1,'count':1,
          'date': {'$dateFromString': {
            'dateString': '$_id',
            'format': "%d/%m/%Y"
          }
        }}},
         { '$sort' : { 'date' : 1} }
        ]
     data_recovered = list(coln.aggregate(agg2))


     agg3=[{'$match':{'$and':[{'dateannounced':{'$ne':""}},  {'currentstatus':'Deceased'} ]}},
         {'$group': {'_id': '$dateannounced','count': { '$sum': 1 }}},
        { '$project': {
            'dateannounced':1,'count':1,
          'date': {'$dateFromString': {
            'dateString': '$_id',
            'format': "%d/%m/%Y"
          }
        }}},
         { '$sort' : { 'date' : 1} }
        ]
     data_deceased = list(coln.aggregate(agg3))

     # to get hospitalized data of all the states for current date
     #agg4=[{'$match':{'$and':[{'dateannounced':t_date},  {'currentstatus':'Hospitalized'} ]}},
    #     {'$group': {'_id': '$detectedstate','count': { '$sum': 1 }}},
    #     { '$sort' : { 'count' : -1} }
    #    ]
     #data_statewise = list(coln.aggregate(agg4))


     return [data_confirmed, data_recovered,data_deceased]

def get_age_graph(coln):
    fig, ax = plt.subplots(figsize=(30,18))
    def convert_ages_to_int(data):
         y1=[]
         for h in data:
              #print(h)
              try:
                   v  = int(h['agebracket'])
                   y1.append(v)
              except:
                   #print(h['agebracket'])
                   if h['agebracket'] == "":
                        #y1.append(0)
                        pass
                   elif (len(h['agebracket']) >1 ) and (h['agebracket'].find("-")>-1):
                        v = [int(h['agebracket'].split("-")[0]), int(h['agebracket'].split("-")[1])]
                        y1.append(mean(v))
         return y1

    hospitalized = list(coln.find({'$and':[{'dateannounced':{'$ne':""}},  {'currentstatus':'Hospitalized'} ]}, {'agebracket':1,'_id':0}))
    hosp_data = convert_ages_to_int(hospitalized)

    hospitalized = list(coln.find({'$and':[{'dateannounced':{'$ne':""}},  {'currentstatus':'Recovered'} ]}, {'agebracket':1,'_id':0}))
    reco_data = convert_ages_to_int(hospitalized)

    hospitalized = list(coln.find({'$and':[{'dateannounced':{'$ne':""}},  {'currentstatus':'Deceased'} ]}, {'agebracket':1,'_id':0}))
    deceas_data = convert_ages_to_int(hospitalized)

    age_bucket = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120]
    plt.hist(hosp_data,age_bucket, label='hospitalized',histtype='bar',rwidth=0.8) # calling hist function instead of plot or bar to plot histogram
    plt.hist(reco_data,age_bucket, label='recovered',histtype='bar',rwidth=0.8)
    plt.hist(deceas_data,age_bucket, label='dead',histtype='bar',rwidth=0.8)

    plt.xlabel("Age buckets with interval of 5.")
    plt.ylabel("Number of the patients")
    plt.title("Histogram of number of age wise hospitalized, recovred and deceased covid patients.")
    plt.legend()
    #plt.show()
    plt.savefig(img_dir+"Age wise distribution.png", facecolor='w', edgecolor='w',orientation='portrait')


def daily_bar_graph(data_confirmed):

    fig, ax = plt.subplots(figsize=(30,18))
    #create x and y for plotting
    x= [k['_id'][0:5] for k in data_confirmed]
    y=[k['count'] for k in data_confirmed]

    for idx in range(len(x)):
        plt.text(x[idx], y[idx], str(y[idx]))


    plt.plot(x,y, label="line graph", color='r')
    plt.bar(x,y, label="bar graph", color='c')
    plt.xlabel("date of the patients confirmation")
    plt.xlabel("number of the patients confirmed")
    plt.title(f"Confirmed ({sum(y)}) corona virus cases in India")
    plt.legend()
    plt.gcf().autofmt_xdate()
    #plt.show()
    plt.savefig(img_dir+"Confirmed.png", facecolor='w', edgecolor='w',orientation='portrait')

def daily_graph_recovered(data_recovered):
    #let us get the unique new patients by date
    fig, ax = plt.subplots(figsize=(30,18))

    #create x and y for plotting
    x= [k['_id'][0:5] for k in data_recovered]
    y=[k['count'] for k in data_recovered]

    for idx in range(len(x)):
        plt.text(x[idx], y[idx], str(y[idx]))


    plt.plot(x,y, label="line graph", color='r')
    plt.bar(x,y, label="bar graph", color='c')
    plt.xlabel("date of the patients recovered")
    plt.xlabel("number of the patients recovered")
    plt.title(f"Recovered ({sum(y)}) corona virus cases in India")
    plt.legend()
    plt.gcf().autofmt_xdate()
    #plt.show()
    plt.savefig(img_dir+"Recovered.png", facecolor='w', edgecolor='w',orientation='portrait')

def daily_graph_deceased(data_deceased):
    #let us get the unique new patients by date

    fig, ax = plt.subplots(figsize=(30,18))

    #create x and y for plotting
    x= [k['_id'][0:5] for k in data_deceased]
    y=[k['count'] for k in data_deceased]

    for idx in range(len(x)):
        plt.text(x[idx], y[idx], str(y[idx]))

    plt.plot(x,y, label="line graph", color='r')
    plt.bar(x,y, label="bar graph", color='c')
    plt.xlabel("date of the patients deceased")
    plt.xlabel("number of the patients deceased")
    plt.title(f"Deceased ({sum(y)}) corona virus cases in India")
    plt.legend()
    plt.gcf().autofmt_xdate()
    #plt.show()
    plt.savefig(img_dir+"Deceased.png", facecolor='w', edgecolor='w',orientation='portrait')

def daily_all_cases_bar(all_data):
    # set width of bar
    barWidth = 0.25

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(30,18))

    x= [k['_id'][0:5] for k in all_data[0]]
    y1 = [k['count'] for k in all_data[0]]

    y,y2=[],[]
    x2,y = [k['_id'][0:5] for k in all_data[1]], [k['count'] for k in all_data[1]]

    for i in range(len(x)):
        if x[i] in x2:
            index = x2.index(x[i])
            y2.append(y[index])
        else:
            y2.append(0)
    y,y3=[],[]
    x3,y = [k['_id'][0:5] for k in all_data[2]], [k['count'] for k in all_data[2]]
    for i in range(len(x)):
        if x[i] in x3:
            index = x3.index(x[i])
            y3.append(y[index])
        else:
            y3.append(0)

    #x2= [k['_id'][0:5] for k in all_data[2]]
    #y2=[k['count'] for k in all_data[2]]

    pos = list(range(len(x)))

    # Make the plot
    plt.bar(pos,y1, color='#EE3224', width=barWidth, alpha=0.5, edgecolor='white', label='infacted')
    plt.bar([p + barWidth for p in pos],y2, color='#F78F1E', width=barWidth, alpha=0.5, edgecolor='white', label='recovered')
    plt.bar([p + barWidth*2 for p in pos], y3, color='#FFC222', width=barWidth,edgecolor='white',alpha=0.5,  label='deceased')

    plt.scatter(x,y1, label="infacted", color='b')
    plt.scatter(x,y2, label="recovered", color='g')
    plt.scatter(x,y3, label="deceased", color='r')


    for idx in range(len(x)):
        plt.text(x[idx], y3[idx], str(y3[idx]))

    for idx in range(len(x)):
        plt.text(x[idx], y1[idx], str(y1[idx]))

    # Add xticks on the middle of the group bars
    plt.xlabel('Gourp bar plot dates', fontweight='bold')
    plt.ylabel('number of patients', fontweight='bold')
    #plt.xticks([r + barWidth for r in range(len(bars1))], ['A', 'B', 'C', 'D', 'E'])
    # Create legend & Show graphic

    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * barWidth for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(x)

    #Setting the x-axis and y-axis limits
    #print(min(pos)-barWidth, max(pos)+(barWidth*4))
    plt.xlim(min(pos)-barWidth, max(pos)+(barWidth*4))
    plt.ylim([0, max(y1+ y2 +y3)] )
    plt.gcf().autofmt_xdate()

    plt.title(f"Infacted-({sum(y1)}), Recovred({sum(y2)}), Deceased ({sum(y3)}), Active ({(sum(y1)-(sum(y2)+sum(y3)))}) corona virus cases in India")
    plt.legend()
    plt.grid()
    #plt.show()
    plt.savefig(img_dir+"overall.png", facecolor='w', edgecolor='w',orientation='portrait')

def controller():
    coln = config()
    all_data=get_all_data(coln)
    daily_bar_graph(all_data[0])
    daily_graph_recovered(all_data[1])
    daily_graph_deceased(all_data[2])
    daily_all_cases_bar(all_data)
    get_age_graph(coln)
    deconfig()
if __name__ == "__main__":
    controller()
    #input()
else:
    pass
