from __future__ import division
import csv
import json
import sys


#csvname = sys.argv[1]
#csvfile = open(csvname, 'r')
def convert(csv):
#    csvname = csv
#    csvfile = open(csvname, 'r')
#    filename = csvname[:-4]
#    print(filename)
#    jsonfilename=filename + ".json"
#    jsonfile = open(jsonfilename , 'w')
    fieldnames = ("starttime","recordpath","frequency","length","startearly","logfilepath","gain")
    reader = csv.DictReader( csv, fieldnames)
    for row in reader:
        print(json.dump(row, jsonfile))
    return
#    jsonfile.write('\n')
def main():
    print("This is working")
    print(len(sys.argv))
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as csv:
            convert(csv)
    else:
	print("What?")
    return
if __name__ ==  " __main__":
    main()
