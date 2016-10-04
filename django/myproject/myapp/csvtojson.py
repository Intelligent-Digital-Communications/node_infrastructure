#!/usr/bin/env python
import csv, json, sys

def convert(csvfile):
    fieldnames = ("starttime","recordpath","frequency","length","startearly",
            "logfilepath","gain")
    recordings = []
    master_dict = { 'recordings' : recordings }
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        print(row)
        if not row['starttime'].startswith('#'): # Assumes startime is 1st
            recordings.append(row)
    return json.dumps(master_dict)

if __name__ ==  "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as csv:
            print(convert(csv))
    else:
        print("Give csv name of schedule as parameter.")
