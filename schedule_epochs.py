import sys
import os
import subprocess
import csv
from datetime import datetime # This is the datetime class, not module!

PATHKEY = "--path="
DISPLAYHELPCODE = -461

def print_help():
    print("--------------schedule_epochs.py--------------")
    print(" - Runs a atqCmd files and records all of the jobIDs, times, " +
        "and filenames scheduled.")
    print(" - Parameter '--path=/AAA/BBB/' to specify where the files are.")
    print("   * Be sure that these files contain absolute paths.")
    print("   * Supports multiple cmds, just give multiple --path flags.")
    print("----------------------------------------------")

def process_atqCmd(full_path):
    infile = open(full_path, 'r')
    lines = infile.read().split('\n')
    infile.close()
    for line in lines:
        if line == '':
            # Break when we hit whitespace so that we don't hit the directions
            return
        schedule_epoch(line)

def schedule_epoch(line):
    epoch_path = line.split(' -f ')[1].split(' ')[0]
    # Right after -f tag, nothing after the path.

    # Executes the line and stuffs the output into output and err
    p = subprocess.Popen(
            line.split(' '),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
    output, err = p.communicate() # Catch output in these vars

    if "Cannot open input file" in err:
        print(err)
        return DISPLAYHELPCODE
    # Probably launched the file wrong

    lines = err.split('\n')
    job_misc = lines[1].split(' at ') # 0th line is just a shell warning

    # At this point, job_misc[0] is 'job #' and job_misc[1] is 'Sat Nov...'
    job_id = job_misc[0].split(' ')[1] # Pull the job id
    job_datetime = datetime.strptime(job_misc[1], "%c") # Create datetime object

    print("Job ID " + job_id + " scheduled for " + str(job_datetime))
    # TODO: Log the schedules IDs, filenames, and datetimes to a CSV or database

def main():
    for parameter in sys.argv:
        if PATHKEY in parameter:
            path = parameter.split('=')[1]
            if os.path.exists(path):
                process_atqCmd(path)
        else:
            print_help()
main()
