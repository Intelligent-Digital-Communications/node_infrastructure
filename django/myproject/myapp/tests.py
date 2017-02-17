from django.test import TestCase
from django.test import Client
from django.core import mail
from datetime import datetime, timedelta
from .csvtojson import convert
from .NodeListener import *
#from NodeListener import filedrop
import os
import csv

# Example test for posting a CSV, need to create a jsonSessionDict
'''
class ScheduleAndCancelTestCase(TestCase):
    def test_schedule_then_cancel(self):
        c = Client()
        with open('myproject/myapp/csv/controller_test_schedule.csv', 'rb') as csv:
            response = c.post('/myapp/upload_file/', { 'docfile' : csv, 'rfsns' : [1] })
            self.assertTrue(response.status_code == 200)
            self.assertEqual(len(mail.outbox), 1)
            s = Util.loads(response.content.decode('utf-8'))
            print(s)
'''

class ScheduleSoonAndCancelTestCase(TestCase):
    def test_schedule_soon_then_cancel(self):
        with open('myproject/myapp/csv/controller_test_schedule.csv', 'w', newline='') as csvfile:
            now = datetime.datetime.now()
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #change 1,2,3 to 0 for local testing
            csvwriter.writerow(['TestGame1', '/tmp/' + now.strftime('%H-%M') + '/', 'spring17_test.log', '1', '2', '3'])
            for i in range(1,10):
                csvwriter.writerow([(now + timedelta(minutes=1*i)).strftime('%m/%d/%Y %H:%M'), 
                'epoch_test' + str(i) + '.sc16', '2.41E+09', '3', '60', '55'])
        
        c = Client()
        with open('myproject/myapp/csv/controller_test_schedule.csv', 'rb') as csvfile:
            response = c.post('/myapp/upload_file/', { 'docfile' : csvfile, 'rfsns' : [1] })
            self.assertTrue(response.status_code == 200)
            self.assertEqual(len(mail.outbox), 1)
            s = Util.loads(response.content.decode('utf-8'))
            print(s)

'''
class TestFiledropSession(TestCase):
    def runTest(self):
        c = Client()
        passing = {'spath': '/home/ops/testfolder/', 'rfsnid':'1', 'fpath':'test', 'date':'20161029', 'game':'duke', 'scheduletime': '2:30 PM 11/15/2016'}
        response = c.post('/myapp/filedrop/1/', passing)
        print(response)
        #print(filedrop(json.dumps(passing)))
'''
