from django.test import TestCase
from django.test import Client
from django.core import mail
from datetime import datetime, timedelta
from .csvtojson import convert
from nodelistener import *
from recordingclasses import Recording, Session, Util
from .models import RFSN, RecordingModel, SessionModel
import os
import csv
from subprocess import Popen, call, PIPE

class LocalTest(TestCase):
    def setUp(self):
        #call('startlistener', stdout=PIPE, stderr=PIPE) # Pipes hide output
        RFSN.objects.create(name="localhost", hostname="localhost", port=8000, pk=0)

class DeploymentTest(TestCase):
    def setUp(self):
        RFSN.objects.create(name="localhost", hostname="localhost", port=8000, pk=0)
        RFSN.objects.create(name="rfsn1", hostname="rfsn1", port=5035, pk=1)
        RFSN.objects.create(name="rfsn2", hostname="rfsn2", port=5035, pk=2)
        RFSN.objects.create(name="rfsn3", hostname="rfsn3", port=5035, pk=3)


class ScheduleSoonAndCancelTestCase(LocalTest):
    """Example test for posting a CSV"""

    def test_schedule_soon_then_cancel(self):
        testfile = '/tmp/controller_test_schedule.csv'
        with open(testfile, 'w', newline='') as csvfile:
            now = datetime.now()
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                    quoting=csv.QUOTE_MINIMAL)

            #change 1,2,3 to 0 for local testing
            # Write the session properties
            csvwriter.writerow(['TestGame1', '/tmp/' + now.strftime('%H-%M') + '/',
                'spring17_test.log', '60', '25000000', '0'])

            # Write each recording
            for i in range(1,3):
                csvwriter.writerow([
                    (now + timedelta(minutes=1*i)).strftime('%m/%d/%Y %H:%M'),
                'epoch_test' + str(i) + '.sc16', '2.41E+09', '3', '55'])

        c = Client()
        with open(testfile, 'rb') as csvfile:
            response = c.post('/myapp/upload_file/',
                    { 'docfile' : csvfile, 'rfsns' : [0] })
            self.assertTrue(response.status_code == 200)
            self.assertEqual(len(mail.outbox), 1)
            s = Util.loads(response.content.decode('utf-8'))

class ListRFSNsTest(LocalTest):
    def test_listRFSNs(self):
        c = Client()
        response = c.get("/myapp/list/")

     #def tearDown(self):
     #    print(RecordingModel.objects.all())

class ListRecordingsTestCase(LocalTest):
    def test_list_recordings_test(self):
        self.rate = 25000000
        b = SessionModel(sample_rate=self.rate, start_early=60)
        b.save()
        b.name = "TEST"
        local = RFSN.objects.get(id=0)
        b.rfsns = [local]
        b.log_path = "/dev/null"
        b.starting_path = "/dev/null"
        b.save()
        RecordingModel.objects.create(rfsn=local, session=b, at_datetime=datetime.now(), unix_jobid=1,
            specrec_args_length=60,specrec_args_freq=50502025,specrec_args_gain=45,specrec_args_sample_rate=25000000,
            specrec_args_start=datetime.now(), specrec_args_full_commands='',
            local_path='/dev/null/', backup_path='/dev/null/')


        c = Client()
        response = c.get('/myapp/recording_list/', {"rfsn_id": 0})
        self.assertTrue(str(self.rate) in str(response.content))
        response = c.get('/myapp/recording_list/', {"session_name": "TEST"})
        self.assertTrue(str(self.rate) in str(response.content))
        response = c.get('/myapp/recording_list/')
        self.assertTrue(str(self.rate) in str(response.content))

'''
class TestFiledropSession(TestCase):
    def runTest(self):
        c = Client()
        passing = {'spath': '/home/ops/testfolder/', 'rfsnid':'1', 'fpath':'test', 'date':'20161029',
        'game':'duke', 'scheduletime': '2:30 PM 11/15/2016'}
        response = c.post('/myapp/filedrop/1/', passing)
        print(response)
        #print(filedrop(json.dumps(passing)))
'''

class GetATQTestCase(LocalTest):
    def test_get_atq(self):
        c = Client()
        response = c.get('/myapp/getatq/', {'pk': 0})
        s = Util.loads(response.content)
