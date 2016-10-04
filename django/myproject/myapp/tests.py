from django.test import TestCase
from django.test import Client
from .csvtojson import convert

# Example test for posting a CSV, need to create a jsonSessionDict
c = Client()
with open('myproject/myapp/csv/test0.csv', 'rb') as csv:
    response = c.post('/myapp/upload_file/', { 'docfile' : csv, 'rfsns' : 1 })
    print(response.status_code)
    print(response.content)
