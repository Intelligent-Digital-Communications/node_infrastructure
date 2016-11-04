import sys, os, subprocess, time, datetime, logging, pickle, hug, json
from subprocess import Popen, PIPE
try:
    from .RecordingClasses import Recording, Session, Util
    from .schedule_session import schedule_session
except SystemError:
    from RecordingClasses import Recording, Session, Util
    from schedule_session import schedule_session
LOG_FILENAME = "nodelistener.log"

def help():
    print("\n--------------------------NodeListener.py--------------------------\n"
          "         - This application connects to the RFSN Client,         \n"
          "            updates gains and schedules data captures.           \n"
          "-----------------------------------------------------------------\n")

def update_gains(gainInfo):
    try:
        if not gainInfo[2].endswith("/"):
            path = gainInfo[2] + "/"
        else:
            path = gainInfo[2]
        if not os.path.exists(path):
            return "Invalid path to generate epochs."
    except:
        return "Invalid path to generate epochs."

    try:
        err = os.system("python update_gains.py " + "--gain=" + gainInfo[1] + " --path=" + path)
        if err == 0:
            message = "\nGain for " + str(gethostname()) + " updated!"
        else:
            message = "There was an error updating the gains. Please try again."

        return message
    except:
        return "Error updating gains on the server. Please try again."

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
    try:
        #Recording.recordpath after -av
        print(body)
        jsonData = json.loads(body)
        scheduletime = jsonData['scheduletime']		#2:30 PM 10/21/2014
        date = jsonData['date']         #20161029
        game = jsonData['game']         #duke
        rfsnid = jsonData['rfsnid']     #1
        spath = jsonData['spath']       #/home/ops/testfolder
        fpath = jsonData['fpath']       #test
        commonpath = 'uploader@idc2.vip.gatech.edu:/home/idcjbod/filedrop'

        folderpath = fpath + '/' + date + '_' + game + '/' + 'rfsn' + rfsnid + '/' + 'pred/'        #/test/20161029_duke/rfsn1/pred/
        dpath = commonpath + '/' + folderpath      #uploader@idc2.vip.gatech.edu:/home/idcjbod/filedrop/test/20161029_duke/rfsn1/pred/

	###############################################################################
        logfilepath = '/log'
        args = ('rsync -av {spath} {dpath} >> {logfilepath} 2>&1').format(
        spath=spath, dpath = dpath, logfilepath = logfilepath)

        filename = 'delayedrsync.sh'
        epoch_file = open(filename, 'w')
        epoch_file.write('#!/bin/bash\necho {} >> {}\n{}'
                        .format(filename, logfilepath, args))
        epoch_file.close()
        os.chmod(filename, os.stat(filename).st_mode | int("0111", 8)) # Make exec by everyone	
	#################################################################################
        atargs = ['mkdir', '-p', folderpath]#, '&&', 'rsync', '-av', spath, dpath, '']
        Popen(atargs, stdout=PIPE, stderr=PIPE)
        print(atargs)
        atargs = ['rsync', '-av', fpath, commonpath]
        Popen(atargs, stdout=PIPE, stderr=PIPE)
        print(atargs)
        atargs = ['at', '-f', 'delayedrsync.sh', scheduletime]
        Popen(atargs, stdout=PIPE, stderr=PIPE)
        print(atargs)
        #atargs = ['rsync', '-av', spath, dpath]
        #Popen(atargs, stdout=PIPE, stderr=PIPE)
        #print(atargs)

        

        return 'success'
    except Exception as e:
        return {'log': 'Exception occurred: ' + str(e)}

@hug.post('/get_atq')
def getatq(body):
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


def setup_logger():
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    logging.info(datetime.datetime.now())

if __name__ == "__main__":
    setup_logger()
    main()
