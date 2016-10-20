import os, shutil, stat, sys, datetime, subprocess, json, jsonpickle

class Util(object):
    def __repr__(self):
        return self.__str__()

    def __eq__(self, b):
        return self.__dict__ == b.__dict__

    @staticmethod
    def dumps(recording):
        return jsonpickle.encode(recording)

    @staticmethod
    def loads(dumped):
        return jsonpickle.decode(dumped)

class Recording(Util):
    """ Defines everything you need to know to schedule a record """

    def __init__(self, starttime, recordpath, frequency, length, startearly=40,
            gain=50, uniques=None):
        self.starttime  = datetime.datetime.strptime(starttime, "%m/%d/%Y %H:%M")
        self.recordpath = recordpath # ends in Sc16
        self.frequency = float(frequency)
        self.length = int(length)
        self.startearly = int(startearly)
        self.gain = int(gain)
        if uniques:
            self.uniques = uniques

    def __str__(self):
        return '{} {}'.format(self.recordpath, self.starttime.isoformat())

class Session(Util):
    """ Collection of Recordings and related metadata. """

    def __init__(self, recordings, startingpath, rfsnids, include='include/', logpath='log.txt', name='Default Name'):
        self.logpath = logpath
        self.startingpath = startingpath
        self.rfsnids = rfsnids
        self.recordings = []
        for record in recordings:
            appending = None
            if not type(record) is Recording:
                appending  = Recording(**record)
            else:
                appending = record
            self.recordings.append(appending)

        self.include = include
        self.name = name

    def __str__(self):
        return '{} {}'.format(self.name, str(self.recordings))
