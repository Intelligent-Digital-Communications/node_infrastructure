import os, shutil, stat, sys, datetime, subprocess

class Recording:
    """ Defines everything you need to know to schedule a record """

    def __init__(self, starttime, recordpath, frequency, length, startearly=40,
            gain=50, jobid=None, uniques=None):
        self.starttime  = datetime.datetime.strptime(starttime, "%m/%d/%Y %H:%M")
        self.recordpath = recordpath # ends in Sc16
        self.frequency = float(frequency)
        self.length = int(length)
        self.startearly = int(startearly)
        self.gain = int(gain)
        if jobid:
            self.jobid = int(jobid)
        if uniques:
            self.uniques = uniques

class Session:

    def __init__(self, recordings, startingpath, rfsnid, include='include/', logpath='log.txt'):
        self.logpath = logpath
        self.startingpath = startingpath
        self.rfsnid = rfsnid
        self.recordings = recordings
        
