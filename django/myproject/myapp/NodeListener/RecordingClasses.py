import os, shutil, stat, sys, datetime, subprocess, json, jsonpickle, re

class Util(object):
    def __repr__(self):
        return self.__str__()

    def __eq__(self, b):
        return self.__dict__ == b.__dict__

    @staticmethod
    def dumps(recording):
        return jsonpickle.encode(recording)

    @staticmethod
    def loads(passsed_in):
        sys.modules['RecordingClasses'] = sys.modules[__name__]
        # This patches in the module's actual name to the global level.
        # Possibly wouldn't be needed if module was set up correctly or registered somehow?

        prefix = 'myproject.myapp.NodeListener.'
        possible = jsonpickle.decode(re.sub(prefix, '', passsed_in))

        if isinstance(possible, str):
            return jsonpickle.decode(possible)
        if isinstance(possible, dict): # Try without taking out the prefix...
            possible = jsonpickle.decode(passsed_in)
        # Must have succeeded!
        return possible

class Recording(Util):
    """ Defines everything you need to know to schedule a record """

    def __init__(self, starttime, recordpath, frequency, length,
            gain=50, uniques=None):
        print(starttime)
        self.starttime  = datetime.datetime.strptime(starttime, "%m/%d/%Y %H:%M")
        self.recordpath = recordpath # ends in Sc16
        self.frequency = float(frequency)
        self.length = int(length)
        self.gain = int(gain)
        self.uniques = uniques

    def __str__(self):
        return '{} {}'.format(self.recordpath, self.starttime.isoformat())

class Session(Util):
    """ Collection of Recordings and related metadata. """

    def __init__(self, recordings, startingpath, rfsnids, samplerate, include='include/', logpath='log.txt', name='Default Name', startearly=40):
        self.logpath = logpath
        self.startingpath = startingpath
        self.rfsnids = rfsnids
        self.recordings = []
        self.samplerate = samplerate
        for record in recordings:
            appending = None
            if not type(record) is Recording:
                appending  = Recording(**record)
            else:
                appending = record
            self.recordings.append(appending)

        #this line might be wrong because it was holding up ^recordings when i placed it above
        self.startearly = int(startearly)
        self.include = include
        self.name = name

    def __str__(self):
        return '{} {}'.format(self.name, str(self.recordings))
