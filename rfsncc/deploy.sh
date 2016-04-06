#!/bin/bash
pkill python
sudo git pull
sudo nohup python NodeListener.py &
