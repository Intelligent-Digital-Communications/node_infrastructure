## How to Test
### Listener Endpoint
Launch the Listener locally:
````
hug -f NodeListener.py &
````

Send a request using a browser extension, the website, or curl.
````
curl 0.0.0.0:8000/endpointname
````
<br>

### Controller Endpoint
Add your test to ````myproject/myapp/tests.py```` and do:
````python3 manage.py test```` from the main ````django```` folder.
