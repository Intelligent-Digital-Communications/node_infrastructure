from django.test import TestCase
from django.test import Client
from .csvtojson import convert

# Example test for posting a CSV, need to create a jsonSessionDict
class ScheduleAndCancelTestCase(TestCase):
    def test_schedule_then_cancel(self):
        c = Client()
        with open('myproject/myapp/csv/newSchedule.csv', 'rb') as csv:
            response = c.post('/myapp/upload_file/', { 'docfile' : csv, 'rfsns' : [0] })
            self.assertTrue(response.status_code == 200)
        # Commented out because endpoint doesn't exist in controller yet 
        #response = c.get('/myapp/clear_atq/', { 'rfsns' : 1,2,3 })
        #self.assertTrue(response.status_code == 200)
    
