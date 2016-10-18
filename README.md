## Testing
##### Listener Tests
````python3 listener_tests.py````

##### Controller Endpoint
Add your test to ````myproject/myapp/tests.py```` and do:
````python3 manage.py test```` from the main ````django```` folder.
<br>

## Deployment
##### Listener
Log into nodes using a terminal that supports simultaneous typing to groups of terminals. Connection info on wiki. Then:
<pre>
$ cd node-infrastructure_operations
$ git pull
</pre>

Kill already running listener and run NodeListener.py with 
<pre>
$ pkill hug
$ cd NodeListener
$ nohup hug -f NodeListener.py &
</pre>

##### Controller
Log into idc-dev, connection info on wiki. Then navigate to your repo, likely with:
<pre>
$ cd node-infrastructure_operations
$ git pull
$ cd django
</pre>
Then run the server.
<pre>
$ pkill python
$ nohup python3 manage.py runserver 0.0.0.0:443 &
</pre>
