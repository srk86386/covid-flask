import matplotlib.pyplot as plt
import matplotlib
from statistics import mean
from pathlib import Path # to work with path
import numpy as np
import pandas as pd
img_dir = str(Path(__file__).parents[1])+"/static/images/"

import time
import os,sys
from pymongo import MongoClient
client = MongoClient()
coln = client.covid_db.raw_data
t_date = time.strftime("%d/%m/%Y")

# to get distinct states in db
all_states = coln.distinct('detectedstate',{'dateannounced':{'$ne':""}})

all_data = {}
idx_num=0
index_to_consider = ""
x_axis_data = []
#let us write a program to print the data
for i in range(len(all_states)): #later replace 3 with len(all_states)
    #print(all_states[i])
    agg1=[{'$match':{'$and':[{'dateannounced':{'$ne':""}},  {'currentstatus':'Hospitalized'},{'detectedstate':all_states[i]} ]}}, # reportedOn, status
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
    all_data[all_states[i]]=data_confirmed
    
#print(all_data)
#print(pd.DataFrame(all_data).head())
#make all indexes available in all states
for idx, value in all_data.items():
    x,y = [k['_id'][0:5] for k in value], [k['count'] for k in value]
    if len(x) > idx_num:
        idx_num = len(x)
        index_to_consider = idx
        #x_axis_data = x
x_axis_data = [k['_id'][0:5] for k in all_data[index_to_consider]]

all_data1={}
all_data2={}

for idx, value in all_data.items():
    y,y1=[],[]
    x,y = [k['_id'][0:5] for k in value], [k['count'] for k in value]
    for i in range(len(x_axis_data)):
        if x_axis_data[i] in x:
            index = x.index(x_axis_data[i])
            y1.append(y[index])
        else:
            y1.append(0)
    all_data1[idx]=y1
    

#print(index_to_consider, x_axis_data,all_data1)


#plotting

print(f" counts of states affacted with covid19 {len(all_data1)}")
#fig, axs = plt.subplots(len(all_data1))
i=0
for state,counts in all_data1.items():
    x = x_axis_data[-10:]
    y = counts[-10:]
    state_mean = mean([mean(counts[-10:]),mean(counts[-5:])])
    #print(f"{state} -  mean patients value = {state_mean}")
    all_data2[state] = counts[-1]-state_mean
    plt.plot(x,y, label=state)
    #axs[i].plot(x,y, label=state)    
    #for idx in range(len(x)):
    #    plt.text(x[idx], y[idx], str(y[idx]))
    i+=1
#plt.legend(loc="upper left",
#          bbox_to_anchor=(0, 0.1, 0.5, 1))
print(all_data2)
plt.grid()
plt.show()




#df = pd.DataFrame(data = [],columns=[])
    
    


