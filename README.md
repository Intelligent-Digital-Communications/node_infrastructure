## How to Test
#### Listener Endpoint
Launch the Listener:
````
hug -f NodeListener.py &
````

Send a request using a browser extension, the website, or curl.
````
curl 0.0.0.0:8000/endpointname
````

#### Controller Endpoint
Add your test to ````myproject/myapp/tests.py````!

## What's Next
Copy out from Listener to backup server

Upload button in webapge

Python function that takes list of recording objects, checks that they are in atq and/or recorded files are there (if expected).

<del>Static HTML files to more easily interface with REST API</del>

GET on node's schedule: Query listener's atq, return to Controller, Controller pull actual record info from database. Or if atq info shows which file being run, more robust to parse those files for record info
