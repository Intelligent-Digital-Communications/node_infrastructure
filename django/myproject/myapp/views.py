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

from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def list(request):
    # Handle file upload
    if request.method == 'POST':
        #form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            for rfsnid in request.POST.getlist('rfsns'):
                rfsn = Rfsn.objects.filter(id=rfsnid)[0]
                returned = rfsn.scheduleepochs(newdoc.docfile.name)
                print('sched_epoch return: ' + str(returned))
            #print('Name: ' + request.POST['name'])
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    return render(
        request,
        'list.html',
        { 'form': form, 'csvs': Document.objects.all() }
    )

@csrf_exempt
def schedule_session(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        result = schedule_session(jsonData)
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
def getatq(request, hostname):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        result = getatq()
        return HttpResponse(result)
    return HttpResponse("OK")

def schedule_session(jsonData):
    session = Util.loads(jsonData)
    results = ''
    for rfsn in session.rfsnids:
        req = schedule(session, rfsn)
        status = ''
        if req.status_code == 200:
            status = str(req.status_code) + ' Job scheduled successfully!\n'
            req_session = Util.loads(req.text)
            for i in range(len(session.recordings)):
                current_local_rec = session.recordings[i]
                current_remote_rec = req_session.recordings[i]
                if current_local_rec.uniques == None:
                    current_local_rec.uniques = {}

                rec_model = RecordingModel(rfsn=RFSN.objects.get(pk=rfsn))
                rec_model.specrec_args_freq = current_remote_rec.frequency
                rec_model.specrec_args_length = current_remote_rec.length
                rec_model.specrec_args_start = current_remote_rec.starttime
                rec_model.unix_jobid = current_remote_rec.uniques[jobId]
                rec_model.at_datetime = current_remote_rec.uniques[jobDateTime]
                rec_model.save()
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

class RfsnListView(ListView):
    #model = RFSN
    def get_context_data(self, **kwargs):
        context = super(RfsnListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

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
        return HttpResponse(schedule_session(jsonschedule))
    return render(request, 'main.html')
