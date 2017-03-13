# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django import forms
from .forms import UploadFileForm
from .csvtojson import convert

from .NodeListener import *
import jsonpickle
import json
import re, sys
import requests
from io import TextIOWrapper

from myproject.myapp.models import *
#from myproject.myapp.forms import DocumentForm
from myproject.myapp.RFSNController import schedule
from myproject.myapp.RFSNController import file_drop
from myproject.myapp.RFSNController import getatq
from myproject.myapp.RFSNController import shutdown

from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def list(request):
    rfsn_objects = RFSN.objects.all()
    print("LIST: ", rfsn_objects)
    rfsn_info = {}
    for rfsn in rfsn_objects:
        rfsn_info[rfsn.id] = {"name":rfsn.name,
                                "hostname":rfsn.hostname,
                                "port":rfsn.port}
    print(rfsn_info)
    return HttpResponse(json.dumps(rfsn_info))

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
        print(hostname)
        result = file_drop(data, hostname)
        print(result)
        return HttpResponse(result)
    return HttpResponse("OK")

@csrf_exempt
def getatq(request):
    if request.method == 'GET':
        rfsn_list = RFSN.objects.filter(pk__in=request.GET.getlist('pks'))
        result = getatq(rfsn)
        print(result)
        return result
    return HttpResponse("OK")

@csrf_exempt
def shutdown(request, hostname, command, port):
    if request.method == 'POST':
        result = shutdown(command, hostname, port)
        return result
    return HttpResponse("OK")

@csrf_exempt
def schedule_session(session):

    print(session)
    print("HEYOOO")
    results = ''
    rfsn_list = RFSN.objects.filter(pk__in=session.rfsnids)
    print("IDs looking for {}".format(session.rfsnids))
    print("Matched {}".format(rfsn_list))
    for rfsn in rfsn_list:
        req = schedule(session, rfsn)
        status = ''
        if req.status_code == 200:
            status = str(req.status_code) + ' Job scheduled successfully!\n'
            req_session = Util.loads(req.text)
            print(req_session)
            for i in range(len(session.recordings)):
                current_local_rec = session.recordings[i]
                current_remote_rec = req_session.recordings[i]
                if current_local_rec.uniques == None:
                    current_local_rec.uniques = {}


                rec = RecordingModel(rfsn=rfsn,
                        unix_jobid = current_remote_rec.uniques['jobId'],
                        local_path = 'ERROR', backup_path = 'ERROR',
                        at_datetime = current_remote_rec.uniques['jobDateTime'])
                rec.specrec_args_freq = current_remote_rec.frequency
                rec.specrec_args_length = current_remote_rec.length
                rec.specrec_args_start = current_remote_rec.starttime
                rec.specrec_args_sample_rate = current_remote_rec.samplerate
                rec.save()
                current_local_rec.uniques[rfsn] = current_remote_rec.uniques
        elif req.status_code == 404:
            status = str(req.status_code) + ' URL not found. Make sure NodeListener is running on the RFSN.\n'
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
        print(jsonschedule)
        session = Util.loads(jsonschedule)
        return HttpResponse(schedule_session(session))
    return render(request, 'main.html')