import sys, time, os, pickle, urllib, json
import requests
from django.core.mail import send_mail

DEFAULTPATH = '' # Listener-side path! '' == Local folder of listener.py UNUSED
#listeners = ["localhost", "rfsn-demo1.vip.gatech.edu", "rfsn-demo2.vip.gatech.edu",
#            "rfsn-demo3.vip.gatech.edu"]
listeners = ["localhost:8000", "sn1-wifi.vip.gatech.edu:8094", "sn1-wifi.vip.gatech.edu:8095",
           "sn2-wifi.vip.gatech.edu:8094"]

def help():
    print("--------------------------RFSNController.py----------------------\n"
          "   - This application connects to the selected RFSN nodes,       \n"
          "         updates gains and schedules data captures.              \n"
          "-----------------------------------------------------------------\n")

def updategains(iplist, gain, path=DEFAULTPATH):
    message = '1,' + gain + ',' + path
    return __sendmessages(iplist, message)

def schedule(session, rfsn):
    url = "http://" + listeners[int(rfsn)] + "/generate_epochs/";
    print("SCHEDULE URL: " + url)
    req = requests.post(url, json=session)
    return req
    
#def genericfunction(jsondata, functionname, rfsn):
#    url = "http://" + listeners[int(rfsn)] + functionname;
#    print("SCHEDULE URL: " + url)
#    req = requests.post(url, json=jsondata)
#    print(jsondata)
#    return req

def filedrop(data, rfsn):
    url = "http://" + listeners[int(rfsn)] + "/filedrop/";
    print("CopyPaste URL: " + url)
    req = requests.post(url, json=data)
    return req

if __name__ == "__main__":
    main()
