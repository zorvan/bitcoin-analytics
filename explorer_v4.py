from flask import Flask, request, render_template, url_for
import requests, json
import time

import datetime                      #Amin
#from flaskext.lesscss import lesscss #Amin
from cryptos import *
#btc = Bitcoin(mainnet=True)

app = Flask(__name__)
host_url = "http://178.162.214.41:5000/"
main_url = 'http://127.0.0.1:8332/rest/'

#lesscss(app)                        #Amin

@app.route('/')
def hello_world():
    return render_template("index.html")
#     return "<a href='./info'>zBlock Explorer<a>"


@app.route('/tx/<transaction_id>')
def transaction(transaction_id):
    a = time.time()
#     transaction_id = "42f9df54a39026ccb54362141c41713968f19e1f14949ab6609b03ffa4b7f120"
#     transaction_id = "1ddfc5c5c15fe173561fb28cfdb874076dc5fbbb4b1854447e35636123bf681b"
    url = main_url + "tx/" + transaction_id +'.json'
    tx_response = requests.get(url)
    content = '''<link rel="stylesheet" href="/static/explorer.css">'''
    content += "<h2>Transaction</h2><hr/>"
    content += '''<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js" charset="utf-8"></script>'''
    content += '''<script src="/static/js/toggle.js" charset="utf-8"></script>'''
    content += str(time.time()-a) + " (s) Elapsed Time!<br/><hr/>"
    content += '''<table width='100%'>'''

    result = json.loads(tx_response.content)
    for key, value in result.items():
        if (key in ["txid","hash"]):
            content += ('<tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td><a href="{}tx/{}">{}</a></td></td>'.format(key, str(type(value)), len(str(value)), request.host_url, str(value), str(value)))
    
    
        elif (key in ["vin","vout"] ):
            #content +=("<tr><td>------ "+ key + " ------ </td></tr>")
            content += '''</table>'''
            content += '''<ul class="accordion" > <li>'''
            content += '''<a class="toggle" href="javascript:void(0);">''' + key + '''</a>'''
            content += '''<ul class="inner">'''
    
            content += '''<table>'''  
            for v in value:
                for key2, value2 in v.items():
                    if (key2 in ["txid"]):
                        content += ('<li><tr><td id="txid">{:25}</td><td>{:20}</td><td>{:_<5}</td><td><a href="{}tx/{}">{}</a></td></td></li>'.format(key2, str(type(value2)), len(str(value2)), request.host_url, str(value2), str(value2)))
                    
                    elif (key2 in ["scriptSig","scriptPubKey"]):
                        content += '''</table><li>'''
                        content += '''<a class="toggle" href="javascript:void(0);">''' + key2 + '''</a>'''
                        content += '''<ul class="inner">'''
                        content += '''<div style="overflow-x:auto;"><table>'''  
                        for key3, value3 in value2.items():
                            content += ('<li><tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td>{}</td></tr></li>'.format(key3, str(type(value3)), len(str(value3)), str(value3)))
                        content += '''</table></div><li></ul>'''
                    elif (key2 in ["value"]):
                        content +=('<table><li><tr><td id="value">{:25}</td><td>{:20}</td><td>{:_<5}</td><td id="value">{}</td></tr></li>'.format(key2, str(type(value2)), len(str(value2)), str(value2),str(value2)))
                    else:
                        content +=('<table><li><tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td title="{}">{}</td></tr></li>'.format(key2, str(type(value2)), len(str(value2)), str(value2),str(value2)))
    
            content += "</table></ul></li></ul><table>"       
            #content +=("<tr><td>------ "+ key + " ------ </td></tr>")
        
       
        elif (key in ["blockhash"]):
            content +=('<tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td><a href="{}block/{}">{}</a></td></tr>'.format(key, str(type(value)), len(str(value)), request.host_url, str(value) ,str(value)))

# ----------- Decode Tx Hex ----------------      
#        elif (key=="hex"):
#            content += '''</table><div style="overflow-x:auto;overflow-y:scroll;"><table>'''
#            content +=('<tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td>{}</td></tr><tr><td><pre>{}</pre></td></tr></table></div>'.format(key, str(type(value)), len(str(value)), str(value), json.dumps(deserialize(value), indent=4, sort_keys=True)))

        else:
            content +=('<tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td>{}</td></tr>'.format(key, str(type(value)), len(str(value)), str(value)[:60]))

    
    content += "</table>"
    content += "<hr/><a href='../info'>zBlock Explorer<a>"

    return content


@app.route('/info')
def info():
    url = main_url + 'chaininfo.json'
    chain_response = requests.get(url)
    result = json.loads(chain_response.content)
    
    content = '''<link rel="stylesheet" href="/static/explorer.css">'''
    content += "<h2>zBlock Explorer</h2><hr/><table width='100%'>"
    for key, value in result.items():
        if(key in "bestblockhash"):
            content +='<tr><td>{:20}</td><td>{:20}</td><td>{:_<5}</td><td><a href="{}">{}</a></td></tr>'.format(key, str(type(value)), len(str(value)), request.host_url + "block/" + str(value), str(value))
        else:
            content +='<tr><td>{:20}</td><td>{:20}</td><td>{:_<5}</td><td>{}</td></tr>'.format(key, str(type(value)), len(str(value)), str(value)[:70])
    content += "</table><hr/><a href='./peers'>Peers Count</a> | <a href='./genesis'>Genesis</a> | <a href=./block/"+ result["bestblockhash"]+">Last Block</a>"
    return content

@app.route('/peers')
def peers():
    import pandas as pd
    df = pd.read_csv("peers_db")
    content = "<h2>Peers</h2><hr/>"
    content += "Count visited peers until 06 March 2018 - 18:00 <b><h1>" + str(len(df)) + "</h1></b><hr/>"
    content += "<a href='./info'>zBlock Explorer<a>"

    return content

@app.route('/genesis')
def genesis():
    from flask import Flask,redirect
    return redirect("./block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f", code=302)


@app.route('/block/<block_hash>')
def getblock(block_hash):
    a = time.time()
    url = main_url + "block/" + block_hash +'.json'
    block_response = requests.get(url)
    
    #Amin
    #content = "<style>{}</style>".format(open("explorer.css", "r").read())
    content = '''<link rel="stylesheet" href="/static/explorer.css">'''
    
    content += "<h2>Block</h2><hr/>"
    content += '''<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js" charset="utf-8"></script>'''
    content += '''<script src="/static/js/toggle.js" charset="utf-8"></script>'''
    content += str(time.time()-a) + " (s) Elapsed Time!<br/><hr/>"
    content += '''<table width='100%'>'''

    result = json.loads(block_response.content)
    for key, value in result.items():
        if(key in ["hash","nextblockhash","previousblockhash"]):
            content += '<tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td><a href="{}">{}</a></td></tr>'.format(key, str(type(value)), len(str(value)), request.host_url +"block/" + str(value) ,str(value))
        elif(key=="time"): #Amin
            content += '<tr><td id="time">{:25}</td><td>{:20}</td><td>{:_<5}</td><td id="time">{}</td></tr>'.format(key, str(type(value)),len(str(value)), str(datetime.datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S'))[:60])
        elif(key=="height"): # Amin
            content += '<tr><td id="height">{:25}</td><td>{:20}</td><td>{:_<5}</td><td id="height">{}</td></tr>'.format(key, str(type(value)), len(str(value)), str(value)[:60])
        elif(key!="tx"): # Amin
            content += '<tr><td>{:25}</td><td>{:20}</td><td>{:_<5}</td><td>{}</td></tr>'.format(key, str(type(value)), len(str(value)), str(value)[:60])
    
    #Amin start
    
    content += "</table><hr/>"
#    content += str(len(result["tx"])) + " Transaction(s) in the block: <div class='tx_page'>"
#    for i in range (min(20,len(result["tx"]))):
#        content += "[<a href=/tx/{}>{}</a>],".format(result["tx"][i]["txid"],str(i))
#    if(len(result["tx"])>20):
#        content += "..."
#    content += "</div><hr/><a href='../info'>zBlock Explorer<a>"
    
    
    content += "<a href='../info'>zBlock Explorer</a><hr/>"
    content += str(len(result["tx"])) + " Transaction(s) in the block: "

    
    content += '''<ul class="accordion" > <li>'''
    content += '''<a class="toggle" href="javascript:void(0);">Transactions</a>'''
    content += '''<ul class="inner">'''
    
    for i in range (0,len(result["tx"])):
        content += "<li><a href=/tx/{}>{}</a></li>".format(result["tx"][i]["txid"],"Transaction Num."+str(i+1))

    content += "</ul></li></ul>"

    
    #Amin stop
    
    
    return content

app.run(host="0.0.0.0")

