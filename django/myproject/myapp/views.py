# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django import forms
from django.utils import timezone
from .forms import UploadFileForm
from .csvtojson import convert

from nodelistener import *
from recordingclasses import Recording, Session, Util

import jsonpickle
import json
import re, sys
import requests
from io import TextIOWrapper

from myproject.myapp.models import *
#from myproject.myapp.forms import DocumentForm
from myproject.myapp.RFSNController import schedule
from myproject.myapp.RFSNController import file_drop
from myproject.myapp.RFSNController import shutdown

from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def list_rfsns(request):
    rfsn_objects = RFSN.objects.all()
    rfsn_info = {}
    for rfsn in rfsn_objects:
        rfsn_info[rfsn.id] = {"name":rfsn.name,
                                #"hostname":rfsn.hostname, Hidden because includes username
                                #"port":rfsn.port,
                                "id": rfsn.id}
    return HttpResponse(json.dumps(rfsn_info))

def recording_list(request):
    if request.method == 'GET':
        data = request.GET     # get filter args from post request
        recording_info = {}
        query = {}                                          # dynamically build query
        if "rfsn_id" in data:
            query["rfsn__pk"] = data["rfsn_id"]
        if "session_name" in data and data["session_name"] is not None:
            query["session__name"] = data["session_name"]
        # unpack query arguments to query the DB
        if query:
            recording_objs = RecordingModel.objects.filter(**query)
        else:
            recording_objs = RecordingModel.objects.all()
        for rec in recording_objs:
            recording_info[rec.pk] = {"rfsn":rec.rfsn.pk,
                                        "datetime":str(rec.at_datetime),
                                        "job_id":rec.unix_jobid,
                                        "local_path":rec.local_path,
                                        "backup_path":rec.backup_path,
                                        "length":rec.specrec_args.length,
                                        "freq":rec.specrec_args.freq,
                                        "sample_rate":rec.specrec_args.sample_rate,
                                        "session":rec.session.name,
                                        "gain": rec.specrec_args.gain}
        return HttpResponse(json.dumps(recording_info))

@csrf_exempt
def schedule_a_session(request):
    if request.method == 'POST':
        req = Util.loads(request.body.decode('utf-8'))
        req = Session(**req)
        result = schedule_session(req)
        return HttpResponse(result)
    return HttpResponse("OK")

@csrf_exempt
def filedrop(request, hostname):
    if request.method == 'POST':
        data = request.POST
        result = file_drop(data, hostname)
        return HttpResponse(result)
    return HttpResponse("OK")

@csrf_exempt
def getatq(request):
    if request.method == 'GET':
        rfsn = RFSN.objects.get(pk=request.GET.get('pk'))
        result = requests.get("{}/get_atq/".format(rfsn.conn_info()))
        return HttpResponse(json.dumps(result.json()))
    return HttpResponse("OK")

@csrf_exempt
def shutdown(request, hostname, command, port):
    if request.method == 'POST':
        result = shutdown(command, hostname, port)
        return result
    return HttpResponse("OK")

def fix_tz(a):
    return timezone.make_aware(a, timezone.get_current_timezone())

@csrf_exempt
def schedule_session(session):
    results = ''
    rfsn_list = RFSN.objects.filter(pk__in=session.rfsnids)

    session_db = SessionModel(name=session.name,
            log_path=session.logpath, starting_path=session.startingpath,
            sample_rate = session.samplerate, start_early=session.startearly)
    session_db.save()

    for rfsn in rfsn_list:
        session_db.rfsns.add(rfsn)
        req = schedule(session, rfsn)
        status = ''

        if req.status_code == 200:
            status = str(req.status_code) + ' Job scheduled successfully!\n'
            req_session = Util.loads(Util.loads(req.text))
            for i in range(len(session.recordings)):
                current_local_rec = session.recordings[i]
                current_remote_rec = req_session.recordings[i]
                if current_local_rec.uniques == None:
                    current_local_rec.uniques = {}


                rec = RecordingModel(rfsn=rfsn, session=session_db,
                        unix_jobid = current_remote_rec.uniques['jobId'],
                        local_path = 'ERROR', backup_path = 'ERROR',
                        at_datetime = current_remote_rec.uniques['jobDateTime'])
                # TODO at_datetime isn't Timezone aware, causes RuntimeWarning

                rec.specrec_args_freq = current_remote_rec.frequency
                rec.specrec_args_length = current_remote_rec.length
                rec.specrec_args_gain = current_remote_rec.gain
                rec.specrec_args_sample_rate = req_session.samplerate
                rec.specrec_args_start = fix_tz(current_remote_rec.starttime)
                rec.save()
                current_local_rec.uniques[rfsn] = current_remote_rec.uniques

        elif req.status_code == 404:
            status = str(req.status_code) + ' URL not found. Make sure \
                    NodeListener is running on the RFSN.\n'
        elif req.status_code == 500:
            status = str(req.status_code) + ' Server error occurred.\n'
        results += ('RFSN ' + str(rfsn) + ': ' + str(status))

    send_mail(
        session.name + ' Schedule Result',
        'Results of scheduling recording session for ' + session.name + ":\n"
        + results,
        'idc.gatech@gmail.com',
        ['rgallaway@gatech.edu', 'haydenflinner@gmail.com', 'orindlincoln@gatech.edu',
            'jaison.george@gatech.edu'],
        fail_silently=False
    )
    return jsonpickle.encode(session)

def status(request):
    nodes = Rfsn.objects.all()
    stats = []
    for node in nodes:
        stats.append((node.hostname,node.getstatus()))

    return render(request,'status.html',{'stats':stats})

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['docfile']
        jsonschedule = convert(TextIOWrapper(uploaded_file.file, encoding='utf-8'))
        session = Util.loads(jsonschedule)
        return HttpResponse(schedule_session(session))
    return render(request, 'main.html')
