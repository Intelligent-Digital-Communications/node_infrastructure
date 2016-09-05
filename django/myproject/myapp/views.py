# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms

import json

from myproject.myapp.models import Document, Rfsn
from myproject.myapp.forms import DocumentForm
from myproject.myapp.RFSNController import schedule

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
def schedule_recordings(request, hostname):
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        for x in jsonData['recordings']:
            schedule(x, hostname)
    return HttpResponse("OK")

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


