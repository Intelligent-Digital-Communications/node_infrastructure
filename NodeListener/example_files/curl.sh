#!/bin/bash
./csvtojson.py $1 | curl -d @- http://idc-dev.vip.gatech.edu:443/myapp/schedule_recordings/1/
./csvtojson.py $1 | curl -d @- http://idc-dev.vip.gatech.edu:443/myapp/schedule_recordings/2/
./csvtojson.py $1 | curl -d @- http://idc-dev.vip.gatech.edu:443/myapp/schedule_recordings/3/
