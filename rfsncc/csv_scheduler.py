import os
import stat
import sys
import datetime
import subprocess

def schedule_csv(infile):
    path = os.getcwd() + '/recordings/'
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
	# Parse the specrec datetime into a datetime object
	# TODO Replace with datetime POSIX standard, making code easier to read
	twoitems = time.split(' ')
	dateinfo = twoitems[0].split('-')
	timeinfo = twoitems[1].split(':')
	datetime_object = datetime.datetime(int(dateinfo[0]), int(dateinfo[1]),
	    int(dateinfo[2]), int(timeinfo[0]), int(timeinfo[1]),
	    int(timeinfo[2]))
	# Give datetime object as time to at
	datetime_object = datetime_object - datetime.timedelta(seconds=40)
	atq_timedate_string = (
		fix_one_digit(str(datetime_object.hour)) + ":"
		+ fix_one_digit(str(datetime_object.minute)) + " "
		+ fix_one_digit(str(datetime_object.month)) + "/"
		+ fix_one_digit(str(datetime_object.day)) + "/"
		+ str(datetime_object.year))
	# TODO gain is hardcoded? Find alternative
	argslist = ['specrec',  '--args=master_clock_rate=25e6',
		'--rate=25e6', '--ant=RX2', '--time=' + str(length_of_epochs),
		'--freq=' + frequency, '--gain=50', '--ref=gpsdo',
		'--metadata=true', '--segsize=24999936',
		'--file=' + filename_for_specrec, r'--starttime="' + time + r'"',
		r'>>', path_for_log_file, r'2>&1' ]
	filename = commandspath + 'epoch' + filename_extension + '.sh'
	epoch_file = open(filename, 'w')
	epoch_file.write('#!/bin/bash\n. ~/sdr/setup_env.sh\necho {} >> {}\n{}'
			.format(filename, path_for_log_file, ' '.join(argslist)))
	epoch_file.close()
	keeptrack.append(filename)
	os.chmod(filename, os.stat(filename).st_mode | 0111) # Make exec by everyone
	atqCmd.write('at ' + atq_timedate_string + ' -f ' + filename + '\n')
	p = subprocess.Popen(
	    ['at', atq_timedate_string, '-f', filename],
	    stdout=subprocess.PIPE,
	    stderr=subprocess.PIPE,
	    )
	output, err = p.communicate()
	keeptrack.append( (argslist, output, err ) )
    atqCmd.close()
    return keeptrack

def main():
    if len(sys.argv) > 1:
        __read_csv_from_parameters()
    else:
        # No args run
        help()

def help():
    print("-------generate_epochs.py Information--------")
    print("Takes a CSV file of start times, filename extensions,"
    + " and frequencies.")
    print("Give it a CSV file path and a path to write files to.")
    print("Generates shell scripts for launching specrec according to CSV file\n")
    print("Needed parameters: [CSV filename] [path to write to]")
    print("Example run: python generate_epochs.py /opt/fall15alcornstate/schedule.csv /opt/fall15alcornstate/")
    print("CSV Format: [specrec time string],[extension to epoch],[frequency],[timeForEpoch]")
    print("For example: [2015-10-15 08:00:00,0,2406] would result in an epoch0.sh file")
    print("that would tell specrec to start recording at 2015-10-15 08:00:00")
    print("at frequency 2406.\n")
    print("Default arguments passed to specrec:")
    print("master_clock_rate = 25e6, rate=25e6, ant=RX2, gain=50, ref=gpsdo")
    print("metadata=true, segsize=24999936\n")
    print("Logs are written to [path to write to]/recordings/logs.txt")

def fix_one_digit(string):
    if len(string) == 1:
        return "0" + string
    return string

if __name__ == "__main__":
    main()
