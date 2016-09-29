import sys, os, subprocess, time, datetime, logging, pickle, hug
from schedule_recordings import schedule_recordings, Recording
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
    passinglist = []
    for record in body:
        passinglist.append(Recording(**record))
    try:
        return schedule_recordings(passinglist)
    except Exception as e:
        return {'log': 'Exception occurred: ' + e}

@hug.post('/copy_paste')
def copy_paste():
    try:
        #Recording.recordpath after -av
        atargs = ['mkdir ','/home/idcjbod/filedrop/test ', '&& ','rsync ', '-av ', '/opt/test_copy/ ', 'uploader@idc2.vip.gatech.edu:/home/idcjbod/filedrop/test']
        subprocess.Popen(atargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        return {'log': 'Exception occurred: ' + e}

def setup_logger():
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    logging.info(datetime.datetime.now())

if __name__ == "__main__":
    setup_logger()
    main()
