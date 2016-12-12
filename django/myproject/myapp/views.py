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

from myproject.myapp.models import Document, Rfsn
from myproject.myapp.forms import DocumentForm
from myproject.myapp.RFSNController import schedule
from myproject.myapp.RFSNController import filedrop

from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
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
        #message = request.GET.get('message')
        #print(message)
        jsonData = json.loads(request.body.decode('utf-8'))
        result = filedrop(jsonData)
        return HttpResponse(result)
    #print('TRNKRYNO')
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
                if session.recordings[i].uniques == None:
                    session.recordings[i].uniques = {}
                session.recordings[i].uniques[rfsn] = req_session.recordings[i].uniques
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

from myproject.myapp.models import Rfsn

class RfsnListView(ListView):
    model = Rfsn
    def get_context_data(self, **kwargs):
        context = super(RfsnListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#from myproject.myapp.models import Rfsn

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
    #return HttpResponse('bad2')
    return render(request, 'main.html')
