# -*- coding: utf-8 -*-
from django import forms
from myproject.myapp.models import Rfsn

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a CSV schedule.')
    mylist = [] 
    for rfsn in Rfsn.objects.all():
        if rfsn.isonline():
            print(str(rfsn.id) + " " + str(rfsn.isonline()))
            mylist.append( (rfsn.id, rfsn.hostname) )
    rfsns = forms.MultipleChoiceField(choices=mylist,
            widget=forms.CheckboxSelectMultiple())
    #name = forms.CharField(label='Your name', max_length=100)

class ScheduleForm(forms.Form):
    docfile = forms.FileField(label='Select a CSV.')
    rfsns = forms.ChoiceField(choices=Rfsn.objects.all())

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
