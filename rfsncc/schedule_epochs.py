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
        if line.startswith('#'):
            continue # Passes commented out lines
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
    if 'past' in err:
        print(' '.join(line.split(' ')[1:3]) + ' has already passed.')
        return
    # Probably launched the file wrong

    lines = err.split('\n')
    job_misc = lines[1].split(' at ') # 0th line is just a shell warning

    # At this point, job_misc[0] is 'job #' and job_misc[1] is 'Sat Nov...'
    job_id = job_misc[0].split(' ')[1] # Pull the job id
    job_datetime = datetime.strptime(job_misc[1], "%c") # Create datetime object

    print("Job ID " + job_id + " scheduled for " + str(job_datetime))
    # TODO: Log the schedules IDs, filenames, and datetimes to a CSV or database

def __read_csv():
    path = os.getcwd()
    for line in infile:
        items, time = line.split(','), items[0]
        filename_extension, frequency = items[1], items[2]
        length_of_epochs = items[3].strip()

        # This is the filename for this specific shell script.
        filename = "epoch" + filename_extension + ".sh"
        filename_with_path = path + filename

        epoch_file = open(filename_with_path, 'w')
        epoch_file.write("#!/bin/bash\n")
        epoch_file.write('echo "' + filename + '" >> ' + path_for_log_file
                + '\n')

        filename_for_specrec = (path + "recordings/epoch" + filename_extension
        + ".sc16")

        # TODO gain is hardcoded? Find alternative
        argslist = ['specrec',  '--args=master_clock_rate=25e6',
                '--rate=25e6', '--ant=RX2', '--time=' + str(length_of_epochs),
                '--freq=' + frequency, '--gain=50', '--ref=gpsdo',
                '--metadata=true', '--segsize=24999936',
                '--file=' + filename_for_specrec, '--starttime="' + time + '"',
                '>>', path_for_log_file, '2>&1']

        # Parse the specrec datetime into a datetime object
        twoitems = time.split(' ')
        dateinfo = twoitems[0].split('-')
        timeinfo = twoitems[1].split(':')
        datetime_object = datetime.datetime(int(dateinfo[0]), int(dateinfo[1]),
            int(dateinfo[2]), int(timeinfo[0]), int(timeinfo[1]),
            int(timeinfo[2]))

        # Schedule the epoch about a minute early with __write_epoch_to_atqCmd()
        __write_epoch_to_atqCmd(filename_with_path, datetime_object, atqCmd)

def main():
    for parameter in sys.argv[1:]:
        if PATHKEY in parameter:
            path = parameter.split('=')[1]
            if os.path.exists(path):
                process_atqCmd(path)
        else:
            print_help()
if __name___ = "__main__":
    main()
