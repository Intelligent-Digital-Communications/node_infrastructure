import sys, time, os, pickle, urllib, json, datetime
import requests
from django.core.mail import send_mail
from .NodeListener import *

DEFAULTPATH = '' # Listener-side path! '' == Local folder of listener.py UNUSED
listeners = ["localhost", "rfsn-demo1.vip.gatech.edu:8000", "rfsn-demo2.vip.gatech.edu:8000",
            "rfsn-demo3.vip.gatech.edu:8000"]
#listeners = ["localhost:8000", "sn1-wifi.vip.gatech.edu:8094", "sn1-wifi.vip.gatech.edu:8095",
#           "sn2-wifi.vip.gatech.edu:8094"]

def help():
    print("--------------------------RFSNController.py----------------------\n"
          "   - This application connects to the selected RFSN nodes,       \n"
          "         updates gains and schedules data captures.              \n"
          "-----------------------------------------------------------------\n")

def updategains(iplist, gain, path=DEFAULTPATH):
    message = '1,' + gain + ',' + path
    return __sendmessages(iplist, message)

def schedule(session, rfsn):
    print(rfsn)
    url = "http://" + listeners[int(rfsn)] + "/generate_epochs/";
    print("SCHEDULE URL: " + url)
    req = requests.post(url, data=Util.dumps(session))
    formattedDate = session.recordings[-1].starttime.strftime("%d%m%Y");
    formattedScheduleTime = (session.recordings[-1].starttime.replace(hour=0) + datetime.timedelta(days=1)).strftime("%H:%M %m/%d/%Y");
    data = {'spath': session.startingpath, 'rfsnid': rfsn, 'fpath':'test', 'date': formattedDate, 'game':'gatech', 'scheduletime': formattedScheduleTime }
    result = file_drop(data, rfsn)
    print(result)
    return req

#def genericfunction(jsondata, functionname, rfsn):
#    url = "http://" + listeners[int(rfsn)] + functionname;
#    print("SCHEDULE URL: " + url)
#    req = requests.post(url, json=jsondata)
#    print(jsondata)
#    return req

def file_drop(data, hostname):
    print(data['rfsnid'])
    rfsn = data['rfsnid']
    jsonData = Util.dumps(data)
    url = "http://" + listeners[int(rfsn)] + "/filedrop/"
    print("http://" + "rfsn-demo1.vip.gatech.edu:8000"	+ "/filedrop/")
    print("CopyPaste URL: " + url)
    req = requests.post(url, data=json.dumps(data))
    return req

def getatq():
    url = "http://" + listeners[int(1)] + "/getatq/";
    print("GetATQ URL: " + url)
    req = requests.post(url)
    return req

if __name__ == "__main__":
    main()
