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
    def loads(passed_in):
        try:
            possible = jsonpickle.decode(passed_in)
        except json.decoder.JSONDecodeError as e:
            raise Exception("Malformed JSON: {}".format(passed_in))
        return possible

class Recording(Util):
    """ Defines everything you need to know to schedule a record """

    def __init__(self, starttime, recordpath, frequency, length,
            gain=50, uniques=None):
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

    def __init__(self, recordings, startingpath, rfsnids, include='include/', logpath='log.txt', name='Default Name', startearly=40, samplerate=25e6):
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
