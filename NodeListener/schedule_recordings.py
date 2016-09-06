import os
import stat
import sys
import datetime
import subprocess

class Recording:
    """ Defines everything you need to know to schedule a record """

    def __init__(self, starttime=None, recordpath=None, frequency=0,
            length=0, startearly=40, logfilepath='log.txt', gain=50,
            include='include/*'):
        self.starttime  = datetime.datetime.strptime(starttime, "%m/%d/%Y %H:%M")
        self.recordpath = recordpath # ends in Sc16
        self.frequency = float(frequency)
        self.length = int(length)
        self.startearly = int(startearly)
        self.logfilepath = logfilepath
        self.gain = int(gain)
        self.include = include
    
def schedule_recordings(recordingslist):
    commandspath = '/' + '/'.join(recordingslist[0].recordpath.split('/')[:-1])
    print(commandspath)
    if not os.path.exists(commandspath):
        os.makedirs(commandspath)
    atqCmd = open(commandspath + '/atqCmd.sh', 'w')
    atqCmd.write('#!/bin/bash\n')
    log = []
    for recording in recordingslist:
        # Create folder for the file to go to
        recordfolder = '/' + '/'.join(recording.recordpath.split('/')[:-1])
        print(recordfolder)
        if not os.path.exists(recordfolder):
            os.makedirs(recordfolder)

        datetime_object = recording.starttime - datetime.timedelta(
                seconds=recording.startearly)

        # Write the sh file that calls specrec
        args = ('specrec --args=master_clock_rate=25e6 --rate=25e6 --ant=RX2 '
                '--time={length} --freq={freq} --gain={gain} --ref=gpsdo '
                '--metadata=true --segsize=24999936 --file={specrecfilename} '
                '--starttime="{start}" >> {logfilepath} 2>&1').format(
                length=recording.length, freq=recording.frequency,
                gain=recording.gain, specrecfilename=recording.recordpath,
                start=recording.starttime.isoformat(' '),
                logfilepath = recording.logfilepath)
        filename = recording.recordpath + '.sh'
        epoch_file = open(filename, 'w')
        epoch_file.write('#!/bin/bash\necho {} >> {}\n{}'
                        .format(filename, recording.logfilepath, args))
        epoch_file.close()
        os.chmod(filename, os.stat(filename).st_mode | int("0111", 8)) # Make exec by everyone
        # TODO Set to only be executable by the current user for security

        # Write the .sh file that we schedule with "at" and schedule it
        atargs = ['at', datetime_object.strftime('%H:%M %m/%d/%Y'), '-f', filename]
        atqCmd.write(' '.join(atargs) + '\n')
        p = subprocess.Popen(atargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Parse the result of scheduling it
        output, err = p.communicate()
        output = output.decode('ascii')
        err = err.decode('ascii')

        if "past" in err: # The one you just scheduled is already over!
            raise ValueError(err)
        jobmisc, atdate = err.split('\n')[1].split(' at ')

        info = {
            'jobId' : jobmisc.split(' ')[1],
            'jobDateTime' : datetime.datetime.strptime(atdate, "%c").isoformat()
        }
        log.append(info)
    atqCmd.close()
    return { 'log' : log }

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

if __name__ == "__main__":
    main()
