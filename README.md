# Node Infrastructure - Operations

## What's Next
Refer to [Issues Page](https://github.gatech.edu/hflinner3/node_infrastructure-operations/issues)

## Building/Testing
#### Controller Testing
Navigate to `django` folder and run `python3 manage.py test`.

#### Listener Testing
Navigate to `django/myproject/myapp/NodeListener` and run `python3 schedule_session_tests.py`.

#### Integration Testing
Navigate to `django/myproject/myapp/NodeListener` and run `hug -f NodeListener.py`.
Create a scheduling CSV that schedules on ID 0 instead of 1,2,3 (currently, refer to the end of the first line of the CSV).
Navigate to `django` and run `python3 manage.py runserver 0.0.0.0:8080`.
Click this link: http://localhost:8080

#### Deployment
On RFSNS, simply navigate to NodeListener folder and run `./startlistener.sh`.
On idc-dev, simply navigate to django folder and run `./startserver.sh`.

## FAQ
`Connection refused error`: The Listener isn't running or the Controller is looking at the wrong address for it. If you get this during a Controller test, be sure that you have a Listener running locally.
`ImportError`: You're missing a Python module that we require. `pip3 install {}` where `{}` == the name of the module given in the ImportError.
`I can't reach the Controller page`: Be sure the django server is running on idc-dev, it may be down for upgrades.
