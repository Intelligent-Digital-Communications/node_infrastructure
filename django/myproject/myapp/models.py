# -*- coding: utf-8 -*-
from django.db import models
from composite_field import CompositeField
import os, subprocess
from subprocess import Popen, PIPE

class Document(models.Model):
    docfile = models.FileField(upload_to='documents')

class RFSN(models.Model):
    name = models.CharField(default="RFSN DEFAULT", max_length=200)
    hostname = models.CharField(max_length=500)
    port = models.IntegerField(default=5035)

    # Turning RFSNs on/off = "./rfsn_ctl " + hostname + " " + status

    def getstatus(self): # Untested
        str = (self.hostname).split('.')
        str[0]  = str[0] + '-rly'
        ip = '.'.join(str)
        port = '2101'
        path = '/var/www/html/fkhan39/uploadsite/myproject/myapp/relay_cmds/rfsn_ctl'
        stat, _ = subprocess.Popen([path, ip, port, 'status'], stdout=PIPE, stderr=PIPE).communicate()
        return stat

    def __str__(self):
        return self.hostname

class SpecrecArgField(CompositeField):
    length = models.IntegerField()
    freq = models.IntegerField()
    sample_rate = models.IntegerField()
    start = models.DateTimeField('Specrec begin recording time')
    full_commands = models.CharField(max_length=1000)

class RecordingModel(models.Model):
    rfsn = models.ForeignKey(RFSN, on_delete=models.CASCADE)
    at_datetime = models.DateTimeField('Linux AT start time')
    unix_jobid = models.IntegerField('Job ID', primary_key=True)
    specrec_args = SpecrecArgField()
    local_path = models.CharField(max_length=1000)
    backup_path = models.CharField(max_length=1000)

    def __str__(self):
        return ' '.join(str(self.rfsn), self.at_datetime)
