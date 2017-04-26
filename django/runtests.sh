#!/usr/bin/env bash
startlistener &
sleep .5 
python3 manage.py test
