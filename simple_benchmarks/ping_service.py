from flask import Flask, request
import requests, json
import subprocess as sp
import time
try:
    import urllib.request as urllib2
    from urllib.request import Request
except ImportError:
    import urllib2

    
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/http/<url>')
def check_site(url):
    if ("http" not in url):
        url = "http://" + url
            
    try:
        http_time = time.time()
        req = urllib2.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib2.urlopen(req, timeout=2)
        http_time = time.time() - http_time
        
        return("UP:"+str(http_time))
    except Exception as e:
        return ("ERR!" + str(e))
    
@app.route('/ping/<ip>')
def ping(ip):
    ping_time = time.time()
    status,result = sp.getstatusoutput("ping -c1 -w2 " + ip)
    ping_time = time.time() - ping_time

    if status == 0: 
        return("UP:" + str(ping_time))
    else:
        return("DOWN!")
    
@app.route('/dns/<host>')
def dns(host):
    dns_time = time.time()
    status,result = sp.getstatusoutput("host " + host)
    dns_time = time.time() - dns_time

    if status == 0: 
        return("UP:" + str(dns_time))
    else:
        return("NOT_RESOLVED!")
    
    
app.run(host="0.0.0.0", port="8001")
