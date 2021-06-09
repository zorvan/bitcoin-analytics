
# coding: utf-8

# In[1]:

import requests
import json
import pandas as pd

tenants = None
df = None
stat_dic = {}
stat_list = []

def fetch():
    tenant_url = "http://51.255.213.178:8080/tenant"
    req = requests.get(tenant_url,timeout=5)
    global tenants, stat_list
    stat_list = []
    tenants =  json.loads(req.text)

    for tenant in tenants:
        tenant_stat_url = ("http://myos.ir/{}/stats/json".format(tenant["id"])) 
        req = requests.get(tenant_stat_url ,timeout=5)
        stats =json.loads(req.text)
        stats["tenant_name"] = tenant["id"]
        stat_list.append(stats)

def decode():
    global stat_dic
    stat_dic = {}
    
    for tenant in stat_list:
        for key,value in tenant.items():
            try:
                if (key in stat_dic.keys()):
                    stat_dic[key] = float(stat_dic[key]) + float(value.replace(',',''))
                else:
                    stat_dic[key] = float(value.replace(',',''))
            except:
                pass

    stat_dic["tenant_name"] = "TOTAL" 
    stat_list.append(stat_dic)
#     print (stat_dic)

def process():
    global df
    df = pd.DataFrame.from_records(stat_list)
    df.set_index("tenant_name")


# In[2]:

# fetch()
# decode()
# process()

# print (df.set_index("tenant_name").T)


# In[3]:

from threading import Thread
from time import sleep

def threaded_function():
        print ("running")
        while(True):
            try:
                print ("fetch...")
                fetch()
                print ("decode...")
                decode()
                print ("process...")
                process()
            except:
                print ("Error")
                pass

            sleep(60)
    
thread = Thread(target = threaded_function)
thread.start()
# thread.join()


from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return ("Hello World!")

@app.route('/stats')
def stats():
    return (df.set_index("tenant_name").T.to_html(col_space=100, justify="center"))

app.run(host="0.0.0.0", port="5005")

