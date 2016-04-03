import os
import sys
import datetime
import subprocess

def schedule_csv(infile):
    path = os.getcwd() + '/recordings/'
    path_for_log_file = path + 'log.txt'
    if not os.path.exists(path):
        os.makedirs(path)
    keeptrack = []
    for line in infile:
        items = line.split(',')
        time, filename_extension, frequency= items[0], items[1], items[2]
        length_of_epochs = items[3].strip()

        # This is the filename for this specific shell script.
        filename = "epoch" + filename_extension + ".sh"

        filename_for_specrec = (path + "recordings/epoch" + filename_extension
        + ".sc16")
        # Parse the specrec datetime into a datetime object
        twoitems = time.split(' ')
        dateinfo = twoitems[0].split('-')
        timeinfo = twoitems[1].split(':')
        datetime_object = datetime.datetime(int(dateinfo[0]), int(dateinfo[1]),
            int(dateinfo[2]), int(timeinfo[0]), int(timeinfo[1]),
            int(timeinfo[2]))
        # Give datetime object as time to at
        atq_timedate_string = (
                str(datetime_object- datetime.timedelta(seconds=40))
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
                r'>>', path_for_log_file, r'2>&1', r'|', r'at',
                atq_timedate_string ]
        print(argslist)
        # TODO Crashing HERE VVV Because no specrec? Get it installed! or ssh to nodes!
        p = subprocess.Popen(
            argslist,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        output, err = p.communicate()
        keeptrack.append( (argslist, output ) )
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
