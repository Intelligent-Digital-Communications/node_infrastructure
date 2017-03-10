import unittest, json, jsonpickle, sys
from RecordingClasses import Recording, Session, Util
from schedule_session import schedule_session
from NodeListener import clear_atq, filedrop

class TestGetATQ(unittest.TestCase):
    def runTest(self):
        """Returns job ids that are currently in the atq."""
        try:
            stdout, _ = Popen('./getatq.sh', stdout=subprocess.PIPE).communicate()
            jobids = [int(x) for x in stdout.decode('ascii').split('\n')[:-1]]
            print(json.dumps({ 'JobIds' : jobids}))
            return json.dumps({ 'JobIds' : jobids})
        except Exception as e:
            print({'log': 'Exception occurred: ' + str(e)})
            return {'log': 'Exception occurred: ' + str(e)}

if __name__ == '__main__':
    unittest.main()
