from django.test import TestCase
from django.test import Client
from django.core import mail
from datetime import datetime, timedelta
from .csvtojson import convert
from .NodeListener import *
#from NodeListener import filedrop
import os

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
        with open('myproject/myapp/csv/controller_test_schedule.csv', 'wb') as csv:
            now = datetime.datetime.now()
            now_plus_one = now + timedelta(minute=10)
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            cvswriter.writerow(['TestGame1','/opt/spring17/','spring17_test.log','1','2','3'])
            for i in range(1,10):
                cvswriter.writerow([(now + timedelta(minute=1*i)).strftime('%DD/%MM/%YYYY %H:%M:%S'), 'epoch_test' + str(i) + '.sc16', '2.41E+09','5','60','55'])

'''
class TestFiledropSession(TestCase):
    def runTest(self):
        c = Client()
        passing = {'spath': '/home/ops/testfolder/', 'rfsnid':'1', 'fpath':'test', 'date':'20161029', 'game':'duke', 'scheduletime': '2:30 PM 11/15/2016'}
        response = c.post('/myapp/filedrop/1/', passing)
        print(response)
        #print(filedrop(json.dumps(passing)))
'''
