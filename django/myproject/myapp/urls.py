# -*- coding: utf-8 -*-
from django.conf.urls import url
from myproject.myapp.views import list#, RfsnListView
from myproject.myapp.views import RfsnListView
from myproject.myapp.views import status
from myproject.myapp.views import schedule_recordings
from myproject.myapp.views import upload_file
#from myapp.views import RfsnListView

urlpatterns = [
    url(r'^hi', RfsnListView.as_view(), name='rfsn-list'),
    url(r'^list/$', list, name='list'),
    url(r'^upload_file/$', upload_file, name='upload_file'),
    url(r'^status/$', status, name='status'),
    url(r'^schedule_recordings/(?P<hostname>\w{0,50})/$', schedule_recordings, 
        name='schedule_recordings')
]

