from __future__ import division
import csv
import json
import sys

def convert(csvname):
    print(csvname)
    csvfile = open(csvname)
    firstread = csv.reader(csvfile, "rb" )
    filename = csvname[:-4]
    csvfileedit=filename+"-edited.csv"
    print(csvfileedit)
    firstwrite = csv.writer(open(csvfileedit))
    headers = csv.writer(open("headers.csv"))
    for row in firstread:
        if("filepath" not in row):
            firstwrite.writerow(row)
            print(row)
        else if ("filepath" in row):
            headers.writerow(row)
            print(row)
    filename = csvname[:-4]
    print(filename)
    jsonfilename=filename + ".json"
    jsonfile = open(jsonfilename , 'w')
    fieldnames = ("starttime","recordpath","frequency","length","startearly","logfilepath","gain")
    reader = csv.DictReader(csvfile, fieldnames)
#    print(csvfile)
    for row in reader:
        print(json.dumps(row))
        jsonfile.write('\n')
    return
def main():
    print("This is working")
    print(len(sys.argv))
    if len(sys.argv) > 1:
        csv=sys.argv[1]
        print(csv)
        convert(csv)
    else:
	print("What?")
    return
if __name__ ==  "__main__":
    main()
