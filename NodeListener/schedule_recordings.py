import os
import stat
import sys
import datetime
import subprocess

class Recording:
    """ Defines everything you need to know to schedule a record """

    def __init__(self, timedate=None, recordpath=None, frequency=0,
            length=0, startearly=40):
        self.timedate = timedate
        self.recordpath = filename # ends in Sc16
        self.frequency = frequency
        self.length = length
        self.startearly = startearly
    
def schedule_recordings(infile):
    # files are written to /opt/nameofCSV
    path = infile.name.split('/')[-1].split('.')[0]
    path_for_log_file = path + 'log.txt'
    if not os.path.exists(path):
        os.makedirs(path)
    keeptrack = []
    commandspath = path + 'commands/'
    if not os.path.exists(commandspath):
        os.makedirs(commandspath)
    atqCmd = open(commandspath + 'atqCmd.sh', 'w')
    atqCmd.write('#!/bin/bash\n')
    for line in infile:
	items = line.split(',')
	time, filename_extension, frequency= items[0], items[1], items[2]
	length_of_epochs = items[3].strip()

	filename_for_specrec = path + 'epoch' + filename_extension + ".sc16"
	# Parse the specrec datetime into a datetime object. Does Specrec use
	# POSIX standard? If so, datetime probably supports parsing itself
	# TODO: Offload date parsing to datetime module
	twoitems = time.split(' ')
	dateinfo = twoitems[0].split('-')
	timeinfo = twoitems[1].split(':')
	datetime_object = datetime.datetime(int(dateinfo[0]), int(dateinfo[1]),
	    int(dateinfo[2]), int(timeinfo[0]), int(timeinfo[1]),
	    int(timeinfo[2]))
	# Give datetime object as time to at
	# TODO at supports POSIX standard, find a way to get a POSIX string
	# from datetime object
	datetime_object = datetime_object - datetime.timedelta(seconds=40)
	atq_timedate_string = (
		fix_one_digit(str(datetime_object.hour)) + ":"
		+ fix_one_digit(str(datetime_object.minute)) + " "
		+ fix_one_digit(str(datetime_object.month)) + "/"
		+ fix_one_digit(str(datetime_object.day)) + "/"
		+ str(datetime_object.year))
	# Gain is hardcoded here. Alternative?
	# Frequency is hardcoded to include an "e6" as its what our hardware
	# is optimized for. Remove if want to use different frequencies.
	argslist = ['specrec',  '--args=master_clock_rate=25e6',
		'--rate=25e6', '--ant=RX2', '--time=' + str(length_of_epochs),
		'--freq=' + frequency + 'e6', '--gain=50', '--ref=gpsdo',
		'--metadata=true', '--segsize=24999936',
		'--file=' + filename_for_specrec, r'--starttime="' + time + r'"',
		r'>>', path_for_log_file, r'2>&1' ]
	filename = commandspath + 'epoch' + filename_extension + '.sh'
	envfile = findENVfile()
	# TODO The line below will probably break in Python 3, but if NodeListener
	# doesn't need root then the if statement below can be removed entirely.
        if "ERROR" in envfile:
            keeptrack.append("ERROR: Unable to source Environment File."
		+ " Specrec will fail unless you patch the epoch.sh files to "
		+ "source the path where specrec is installed.")
	epoch_file = open(filename, 'w')
	epoch_file.write('#!/bin/bash\n. {}\necho {} >> {}\n{}'
			.format(envfile, filename, path_for_log_file, ' '.join(argslist)))
	epoch_file.close()
	keeptrack.append(filename)
	os.chmod(filename, os.stat(filename).st_mode | 0111) # Make exec by everyone
	# TODO Set to only be executable by the current user for security
	atqCmd.write('at ' + atq_timedate_string + ' -f ' + filename + '\n')
	p = subprocess.Popen(
	    ['at', atq_timedate_string, '-f', filename],
	    stdout=subprocess.PIPE,
	    stderr=subprocess.PIPE,
	    )
	output, err = p.communicate()
        if 'past' in err:
            keeptrack.append(' '.join(line.split(' ')[1:3]) + ' has already passed.')
            return keeptrack

        lines = err.split('\n')
        job_misc = lines[1].split(' at ') # 0th line is just a shell warning

        # At this point, job_misc[0] is 'job #' and job_misc[1] is 'Sat Nov...'
        job_id = job_misc[0].split(' ')[1] # Pull the job id
        job_datetime = datetime.datetime.strptime(job_misc[1], "%c") # Create datetime object
        keeptrack.append((argslist, job_id, job_datetime ))
    atqCmd.close()
    print("keeptrack:" + str(keeptrack))
    return keeptrack

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as csv:
            schedule_csv(csv)
    else:
        help()

def help():
    print("-------generate_epochs.py Information--------")
    print("Takes a CSV file of start times, filename extensions,"
    + " and frequencies.")
    print("Generates shell scripts for launching specrec according to CSV file\n")
    print("Also schedules the scripts in the 'at' queue.")
    print("Parameters: [CSV filename]")
    print("Example run: python generate_epochs.py /~/csv_files/schedule.csv")
    print("CSV Format: [specrec time string],[extension to epoch],[frequency],[epochLength]")
    print("For example: [2015-10-15 08:00:00,0,2406] would result in an epoch0.sh file")
    print("that would tell specrec to start recording at 2015-10-15 08:00:00")
    print("at frequency 2406.\n")
    print("Default arguments passed to specrec:")
    print("master_clock_rate = 25e6, rate=25e6, ant=RX2, gain=50, ref=gpsdo")
    print("metadata=true, segsize=24999936\n")
    print("Specrec logs are written to [path to write to]/recordings/logs.txt")

def fix_one_digit(string):
    if len(string) == 1:
        return "0" + string
    return string

if __name__ == "__main__":
    main()
