from django.test import TestCase
from django.test import Client
from django.core import mail
from .csvtojson import convert
from .NodeListener import *
import os

# Example test for posting a CSV, need to create a jsonSessionDict
class ScheduleAndCancelTestCase(TestCase):
    def test_schedule_then_cancel(self):
        c = Client()
        with open('myproject/myapp/csv/controller_test_schedule.csv', 'rb') as csv:
            response = c.post('/myapp/upload_file/', { 'docfile' : csv, 'rfsns' : [0] })
            self.assertTrue(response.status_code == 200)
            self.assertEqual(len(mail.outbox), 1)
            s = Util.loads(response.content.decode('utf-8'))
            print(s)
        # Commented out because endpoint doesn't exist in controller yet 
        #response = c.get('/myapp/clear_atq/', { 'rfsns' : 1,2,3 })
        #self.assertTrue(response.status_code == 200)
    
