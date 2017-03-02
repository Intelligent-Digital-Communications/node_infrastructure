import os, shutil, stat, sys, datetime, subprocess
"""
Takes a Session object and schedules it locally.
1. Generates .sh files that execute specrec.
2. Puts those .sh files in the atq just before their given time.
"""

def schedule_session(session):
    print(session)
    recordingslist = session.recordings
    basepath = session.startingpath
    logfilepath = basepath + session.logpath
    print('.sh files being written to {}'.format(basepath))
    if not os.path.exists(basepath):
        os.makedirs(basepath)
    atqCmd = open(basepath + 'atqCmd.sh', 'w') # w to a?
    atqCmd.write('#!/bin/bash\n')
    for recording in recordingslist:
        print(recording)
        at_starttime = recording.starttime - datetime.timedelta(
                seconds=session.startearly)

        # Write the sh file that calls specrec
        args = ('specrec --args=master_clock_rate=25e6 --rate=25e6 --ant=RX2 '
                '--time={length} --freq={freq} --gain={gain} --ref=gpsdo '
                '--metadata=true --segsize=24999936 --file={specrecfilename} '
                '--starttime="{start}" >> {logfilepath} 2>&1').format(
                length=recording.length, freq=recording.frequency,
                gain=recording.gain, specrecfilename=basepath + recording.recordpath,
                start=recording.starttime.isoformat(' '),
                logfilepath = logfilepath)
        filename = basepath + recording.recordpath + '.sh'
        epoch_file = open(filename, 'w')
        epoch_file.write('#!/bin/bash\necho {} >> {}\n{}'
                        .format(filename, logfilepath, args))
        epoch_file.close()
        os.chmod(filename, os.stat(filename).st_mode | int("0111", 8)) # Make exec by everyone
        # TODO Set to only be executable by the current user?

        # Write the .sh file that we schedule with "at" and schedule it
        atargs = ['at', at_starttime.strftime('%H:%M %m/%d/%Y'), '-f', filename]
        atqCmd.write(' '.join(atargs) + '\n')
        p = subprocess.Popen(atargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Parse the result of scheduling it
        output, err = p.communicate()
        output = output.decode('ascii')
        err = err.decode('ascii')

        if "past" in err: # The one you just scheduled is already over!
            raise ValueError(err)
        jobmisc, atdate = err.split('\n')[1].split(' at ')

        recording.uniques = {
            'jobId' : int(jobmisc.split(' ')[1]),
            'jobDateTime' : datetime.datetime.strptime(atdate, "%c").isoformat()
        }
    atqCmd.close()
    copyfolder(session.include, basepath)
    return session

def copyfolder(src, dest):
    for filename in os.listdir(src):
        fullsrcpath = os.path.join(src, filename)
        if os.path.isfile(fullsrcpath):
            shutil.copy(fullsrcpath, dest)

if __name__ == "__main__":
    print('This module does not support being run from the command line.')
