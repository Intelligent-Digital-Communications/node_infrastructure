# -*- coding: utf-8 -*-
from django.conf.urls import url
from myproject.myapp.views import list#, RfsnListView
from myproject.myapp.views import RfsnListView
from myproject.myapp.views import status
from myproject.myapp.views import schedule_session, schedule_a_session
from myproject.myapp.views import upload_file
from myproject.myapp.views import filedrop
from myproject.myapp.views import getatq
#from myapp.views import RfsnListView

urlpatterns = [
    url(r'^hi', RfsnListView.as_view(), name='rfsn-list'),
    url(r'^list/$', list, name='list'),
    url(r'^upload_file/$', upload_file, name='upload_file'),
    url(r'^status/$', status, name='status'),
    url(r'^schedule_session/(?P<hostname>\w{0,50})/$', schedule_session,
        name='schedule_session'),
    url(r'^filedrop/(?P<hostname>\w{0,50})/$', filedrop, name='filedrop'),
    url(r'^getatq/(?P<hostname>\w{0,50})/$', getatq, name='getatq'),
    url(r'^schedule_form/$', schedule_a_session, name='schedule_a_session')
]
