import os
import stat
import sys
import datetime
import subprocess

class Recording:
    """ Defines everything you need to know to schedule a record """

    def __init__(self, starttime=None, recordpath=None, frequency=0,
            length=0, startearly=40, logfilepath='log.txt', gain=50):
        self.starttime = starttime
        self.recordpath = filename # ends in Sc16
        self.frequency = frequency
        self.length = length
        self.startearly = startearly
        self.logfilepath = logfilepath
        self.gain = gain
    
def schedule_recordings(recordingslist):
    commandspath = path + 'commands/'
    if not os.path.exists(commandspath):
        os.makedirs(commandspath)
    atqCmd = open(commandspath + 'atqCmd.sh', 'w')
    atqCmd.write('#!/bin/bash\n')
    for recording in recordingslist:
        path_for_log_file = recording.logfilepath
        recordfolder = recording.recordpath.split('/')[-1].split('.')[0]
        if not os.path.exists(recordfolder):
            os.makedirs(recordfolder)
        time, filename_extension, frequency= items[0], items[1], items[2]
        length_of_epochs = items[3].strip()
        filename_for_specrec = recording.recordpath
        datetime_object = recording.start - datetime.timedelta(
                seconds=recording.startearly)

        atq_timedate_string = datetime_object.strftime('%H:%M %m/%d/%Y')

        args = 'specrec --args=master_clock_rate=25e6 --rate=25e6 --ant=RX2 \
                --time={length} --freq={frequency} --gain={gain} --ref=gpsdo \
                --metadata=true --segsize=24999936 --file={specrecfilename} \
                --starttime="{start}" >> {logfilepath} 2>&1'.format(
                length=recording.length, freq=recording.frequency,
                gain=recording.gain, specrecfilename=recording.recordpath,
                start=recording.starttime.isoformat(' '),
                logfilepath = recording.logfilepath)
        filename = commandspath + 'epoch' + filename_extension + '.sh'
        epoch_file = open(filename, 'w')
        epoch_file.write('#!/bin/bash\n. {}\necho {} >> {}\n{}'
                        .format(envfile, filename, path_for_log_file, ' '.join(argslist)))
        epoch_file.close()
        os.chmod(filename, os.stat(filename).st_mode | int("0111", 8)) # Make exec by everyone
        # TODO Set to only be executable by the current user for security
        atqCmd.write('at ' + atq_timedate_string + ' -f ' + filename + '\n')
        p = subprocess.Popen(
            ['at', atq_timedate_string, '-f', filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        output, err = p.communicate()
        if 'past' in err:
            pass
            # The one you just scheduled is already over!

        lines = err.split('\n')
        job_misc = lines[1].split(' at ') # 0th line is just a shell warning

        # At this point, job_misc[0] is 'job #' and job_misc[1] is 'Sat Nov...'
        job_id = job_misc[0].split(' ')[1] # Pull the job id
        job_datetime = datetime.datetime.strptime(job_misc[1], "%c") # Create datetime object
    atqCmd.close()

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
