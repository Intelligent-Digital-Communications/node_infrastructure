#!/usr/bin/env python
import sys, subprocess

def scp(variable):
    subprocess.Popen("scp " + Recording.recordPath + " ymanoharan3@idc-dev.vip.gatech.edu:/home/storage/")

if __name__ ==  "__main__":
    if len(sys.argv) > 1:
        print(convert(sys.argv[1]))
    else:
	print("variable is missing")
