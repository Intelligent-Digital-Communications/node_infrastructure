#!/usr/bin/env python
import csv, json, sys

def convert(csvname):
    with open(csvname, 'r') as csvfile:
        fieldnames = ("starttime","recordpath","frequency","length","startearly",
                "logfilepath","gain")
        recordings = []
        master_dict = { 'recordings' : recordings }
        reader = csv.DictReader(csvfile, fieldnames)
        for row in reader:
            if not row['starttime'].startswith('#'): # Assumes startime is 1st
                recordings.append(row)
    return json.dumps(master_dict)

if __name__ ==  "__main__":
    if len(sys.argv) > 1:
        print(convert(sys.argv[1]))
    else:
	print("Give csv name of schedule as parameter.")
