# -*- coding: utf-8 -*-
from django.conf.urls import url
from myproject.myapp.views import list#, RfsnListView
from myproject.myapp.views import RfsnListView
from myproject.myapp.views import status
#from myapp.views import RfsnListView

urlpatterns = [
    url(r'^hi', RfsnListView.as_view(), name='rfsn-list'),
    url(r'^list/$', list, name='list'),
    url(r'^status/$', status, name='status'),
]

