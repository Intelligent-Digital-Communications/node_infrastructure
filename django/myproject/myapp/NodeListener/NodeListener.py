import sys, os, subprocess, time, datetime, logging, pickle, hug, json
from subprocess import Popen, PIPE
try:
    from .RecordingClasses import Recording, Session, Util
    from .schedule_session import schedule_session
except SystemError:
    from RecordingClasses import Recording, Session, Util
    from schedule_session import schedule_session

"""
This REST API runs on the nodes in the stadium and awaits commands from the
controlling server, such as scheduling a specrec record.
"""

@hug.post('/generate_epochs')
def generate_epochs(body):
    session = Util.loads(body)
    try:
        return Util.dumps(schedule_session(session))
    except Exception as e:
        return {'log': 'Exception occurred: ' + str(e)} # TODO RETURN 500
        raise e

@hug.post('/filedrop')
def filedrop(body):
    """Schedules a copy of given path to the backup server."""
    try:
        print(body)
        jsonData = json.loads(body)
        scheduletime = jsonData['scheduletime']		#2:30 PM 10/21/2014
        date = jsonData['date']         #20161029
        game = jsonData['game']         #duke
        rfsnid = jsonData['rfsnid']     #1
        spath = jsonData['spath']       #/home/ops/testfolder
        fpath = jsonData['fpath']       #test
        commonpath = 'uploader@idc2.vip.gatech.edu:/home/idcjbod/filedrop'

        folderpath = '{}/{}_{}/{}/pred/'.format(fpath, date, game, str(rfsnid))
        # folderpath = /test/20161029_duke/rfsn1/pred/
        dpath = commonpath + '/' + folderpath
        # dpath = uploader@idc2.vip.gatech.edu:/home/idcjbod/filedrop/test/20161029_duke/rfsn1/pred/


        filename = spath +'/' + 'delayedrsync.sh'
        epoch_file = open(filename, 'w')
        args = ('rsync -av {spath} {dpath} & &>> output.txt').format(spath=spath, dpath=dpath)
        epoch_file.write('#!/bin/bash\necho {}\n{}'.format(filename, args))
        epoch_file.close()
        os.chmod(filename, os.stat(filename).st_mode | int("0111", 8)) # Make exec by everyone	


        # Make the directory locally
        mkdir_args = ['mkdir', '-p', folderpath]
        Popen(mkdir_args, stdout=PIPE, stderr=PIPE)
        print(mkdir_args)

        # Copy that directory off to backup server
        rsync_dir_args = ['rsync', '-av', fpath, commonpath]
        Popen(rsync_dir_args, stdout=PIPE, stderr=PIPE)
        print(rsync_dir_args)

        # Schedule the copy-back
        atargs = ['at', '-f', spath + '/'+ 'delayedrsync.sh', scheduletime]
        stdout, stderr = Popen(atargs, stdout=PIPE, stderr=PIPE).communicate()
        print(stderr.decode('ascii'))
        print(stdout.decode('ascii'))
        return 'success'
    except Exception as e:
        return {'log': 'Exception occurred: ' + str(e)}

@hug.post('/get_atq')
def getatq(body):
    """Returns job ids that are currently in the atq."""
    try:
        stdout, _ = Popen('./getatq.sh', stdout=subprocess.PIPE).communicate()
        jobids = [int(x) for x in stdout.decode('ascii').split('\n')[:-1]]
        return json.dumps({ 'JobIds' : jobids})
    except Exception as e:
        return {'log': 'Exception occurred: ' + str(e)}

@hug.get('/clear_atq')
def clear_atq():
    stdout, _ = Popen('./clearatq.sh', stdout=subprocess.PIPE).communicate()
    jobids = [int(x) for x in stdout.decode('ascii').split('\n')[:-1]]
    return json.dumps({ 'cancelledJobIds' : jobids})

if __name__ == '__main__':
    print("Please refer to the README to use this file.")
