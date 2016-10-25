#!/usr/bin/env python
import csv, json, sys
from .NodeListener import *

def convert(csvfile):
    fieldnames = ["starttime","recordpath","frequency","length","startearly", "gain"]
    recordings = []
    reader = csv.reader(csvfile, fieldnames)
    vals = next(reader)
    for row in reader:
        if not row[0].startswith('#'): # Assumes startime is 1st
            record = {}
            for index in range(len(row)):
                record[fieldnames[index]] = row[index]
            recordings.append(record)

    master_dict = { 'recordings' : recordings,
            'name'      : vals[0],
            'startingpath'  : vals[1],
            'logpath'       : vals[2],
            'rfsnids'       : [int(x) for x in vals[3:]] }
    # TODO Create session, recordings, use Util encoder.

    return json.dumps(master_dict)

if __name__ ==  "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as csvfile:
            print(convert(csvfile))
    else:
        print("Give csv name of schedule as parameter.")
