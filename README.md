# Node Infrastructure - Operations

## What's Next
Refer to [Issues Page](https://github.gatech.edu/IDC/node_infrastructure/issues)

## Building/Testing
#### Controller Testing
Navigate to `django` folder and run `python3 manage.py test`. Don't forget to have the Listener running on localhost!

#### Listener Testing
Go to `idcnodelistener` and run `python3 setup.py test`.

#### Integration Testing
1. Go to `idcnodelistener` and run `startlistener`.
  * [If testing something involving scheduling] Create a scheduling CSV that schedules on ID 0 instead of 1,2,3 (currently, refer to the end of the first line of the CSV).
2. Navigate to `django` and run `python3 manage.py runserver 0.0.0.0:8080`.
3. Click this link: http://localhost:8080

#### Deployment
On RFSNS, navigate to nodelistener package folder and run `nohup startlistener &`.

On idc-dev, navigate to django folder and run `sudo nohup python3 manage.py runserver 0.0.0.0:443 &`.

## FAQ
`Connection refused error`: The Listener isn't running or the Controller is looking at the wrong address for it. If you get this during a Controller test, be sure that you have a Listener running locally.

`ImportError`: You're missing a Python module that we require. `pip3 install {}` where `{}` == the name of the module given in the ImportError.

`I can't reach the Controller page`: Be sure the django server is running on idc-dev, it may be down for upgrades.
