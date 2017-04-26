import sys, time, os, pickle, urllib, json, datetime
import requests
from myproject.myapp.models import *
from django.core.mail import send_mail
from nodelistener import *
from recordingclasses import *

""" Issues commands to NodeListeners. """

def schedule(session, rfsn):
    """Schedules a Session on an RFSN."""
    url = "{}/generate_epochs/".format(rfsn.conn_info())
    req = requests.post(url, data=Util.dumps(session))
    # TODO: Add a check for whether or not we're doing copy-back before calling file_drop
    # Until then, disabled.
    # file_drop(session, rfsn)
    return req

def file_drop(session, rfsn):
    """Schedules a copy-back of recorded data the day after records."""
    last_time = session.recordings[-1].starttime
    formatted_date = last_time.strftime("%d%m%Y")
    hour = ((rfsn.pk-1) * 2) % 8 # Never start copying later than 8AM
    if hour < 0:
        #Probably local testing because rfsn = 0, log it and replace
        print("ERROR: Copy-back schedule time failed! Scheduling for 2:00AM...")
        hour = 2
    formatted_schedule_time = (last_time.replace(hour=hour)
        + datetime.timedelta(days=1)).strftime("%H:%M %m/%d/%Y")
    data = {'spath': session.startingpath, 'rfsnid': rfsn.pk, 'fpath':'test',
        'date': formatted_date, 'game':'gatech', 'scheduletime': formatted_schedule_time, }
    json_data = Util.dumps(data)
    url = "http://{}:{}/filedrop/".format(rfsn.hostname, rfsn.port)
    req = requests.post(url, data=json_data)
    return req

def shutdown(command, rfsn, port):
    if command == "on":
        mkdir_args = ['cat', 'relay_cmds/relay_bank1relay0_on.hex', '|', 'nc', rfsn, port, '|', 'hexdump', '-C']
        Popen(mkdir_args, stdout=PIPE, stderr=PIPE)
        print(mkdir_args)
    elif command == "off":
        #add extra line for shutting down, waiting until the node shuts down, and then running line below
        mkdir_args = ['cat', 'relay_cmds/relay_bank1relay0_off.hex', '|', 'nc', rfsn, port, '|', 'hexdump', '-C']
        Popen(mkdir_args, stdout=PIPE, stderr=PIPE)
        print(mkdir_args)
    elif command == "status":
        mkdir_args = ['cat', 'relay_cmds/relay_status.hex', '|', 'nc', rfsn, port, '|', 'hexdump', '-C']
        Popen(mkdir_args, stdout=PIPE, stderr=PIPE)
        print(mkdir_args)
    else:
        print("Invalid Command: Should be either 'on', 'off', 'status'")
