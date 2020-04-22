from pymongo import MongoClient
import pymongo

client = MongoClient()
db = client.covid_db

import urllib.request, json

urls = ['https://api.rootnet.in/covid19-in/unofficial/covid19india.org',
        'https://api.covid19india.org/raw_data.json',
        'https://api.covid19india.org/data.json',
        'https://api.covid19india.org/travel_history.json',
        'https://api.covid19india.org/states_daily.json',
        'https://api.covid19india.org/state_district_wise.json']

collections = ['rawPatientData','raw_data','cases_time_series','travel_history','states_daily','state_district_wise_']

#let us remove all previous docs
def remove_docs():
    for i in range(len(collections)):
        #print(db[collections[i]].count())
        db[collections[i]].remove()
        #print(db[collections[i]].count())
#remove_docs()
#print(collections)

def reverse_collection():
    data = list(db[collection].find())
    data.reverse()
    db[collection].remove()
    db[collection].insert_many(data)


def change_data_type(collection,field,dtype, sort=False):
    print(f"changing {field} to {dtype} from colllection {collection}")
    data = db[collection].find()
    if dtype=='int':
        for doc in data:
            db[collection].update_one({'_id': doc['_id'] },{ '$set': { field: int(doc[field]) }})
            #db[collection].update({'_id': doc['_id'] },{ '$toInt': "'$"+field+"'"})
            #db[collection].update({'_id': doc['_id'] },{ '$convert': {input: "'$"+field+"'", 'to': 'int','onError': '','onNull':''}})
    elif dtype=='dt':
        for doc in data:
            #col.update({'_id': doc['_id'] },{ '$set': {'tmstamp':timestamp}})
            timestamp = datetime.strptime(doc[field], '%a, %d %b %Y %I:%M:%S %p').strftime('%Y%m%d%H%M%S')
            db[collection].update_one({'_id': doc['_id'] },{ '$set': { field: int(doc[field]) }})


    #if sort:
    #    data = db[collection].find()

def some_fun(d):
    keys=[]
    vals = []
    key_vals=[]
    last_key = []
    json_string=[]
    key_but_value=[False,True]
    def dict_looup(d):
        keys_lenght = len(d.items())
        #print("all keys length",keys_lenght)
        for k, v in d.items():
            if isinstance(v, dict):
                #doc[k.replace(".","_")] ={}
                keys.append(k.replace(".","_"))
                last_key.append('f')
                #key_but_value.append('t')
                if last_key[-1]=='t':
                    json_string.append(" '" + k +"': ")
                else:
                    json_string.append(" {'" + k +"': ")
                #print("key -"+k+ " -"+str(d[k].keys()))
                dict_looup(v)
            else:
                vals.append(v)

                if keys_lenght==len(d.items()) and keys_lenght!=1:
                    json_string.append(" {'" + str(k) +"' "+": '" + str(v) +"', ")
                elif keys_lenght==len(d.items()) and keys_lenght==1:
                    #print(json_string[-1])
                    json_string[-1]=json_string[-1].replace("{","")
                    json_string.append(" {'" + str(k) +"' "+": '" + str(v) +"'}}, ")
                else:
                    json_string.append(" '" + str(k) +"' "+": '" + str(v) +"', ")

                #print(json_string)
                #print(keys_lenght,len(d.items()))
                keys_lenght-=1
                #key_vals.append((last_key[-1],{k:v}))
                if len(d.items())-keys_lenght:
                    #key_but_value=True
                    last_key.append('t')
                #print("{0} : {1}".format(k, v))
                pass
        #json_string.append("},")
        #print("====================")
        #print(keys, vals,key_vals)
        #print(" ".join(json_string))
        #print(json_string)
        #print("--------------------")
    dict_looup(d)
    json_string[-1] = json_string[-1].replace(",","")
    data_to_return=" ".join(json_string)
    data_to_return = data_to_return+"}}"
    return data_to_return
def get_data():
    remove_docs()
    for i in range(0,4):
        with urllib.request.urlopen(urls[i]) as url:
            data = json.loads(url.read().decode())
            col_name = collections[i]
            if col_name == 'rawPatientData':
                all_docs = list(data['data'][col_name])
                all_docs.reverse()
                current_count = db[col_name].count()
                db[col_name].insert_many(all_docs)
            else:
                all_docs = list(data[col_name])
                current_count = db[col_name].count()
                all_docs.reverse()
                db[col_name].insert_many(all_docs)
            if col_name == 'raw_data':
                #change_data_type(col_name, 'patientnumber', 'int')
                pass
            else:
                pass
            print(f" in if current docs count in collection - {collections[i]} is {current_count}, new count of docs on server {len(all_docs)}")
            pass
            #if len(all_docs)>current_count:
            #    print(f" in if current docs count in collection - {collections[i]} is {current_count}, new count of docs on server {len(all_docs)}")
            #    db[collections[i]].insert_many(all_docs)
            #else:
            #    print(f"current docs count in collection - {collections[i]} is {current_count}, new count of docs on server {len(all_docs)}")
            #    pass

    with urllib.request.urlopen(urls[-1]) as url:
        data = json.loads(url.read().decode())
        for k in data.keys():
            db[collections[-1]].insert_one({f'{k}':some_fun(data[k])})
    print(f"{collections[-1]} collection count is {db[collections[-1]].count()}")
if __name__ == '__main__':
    get_data()
else:
    pass
