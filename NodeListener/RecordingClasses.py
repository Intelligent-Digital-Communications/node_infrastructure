import os, shutil, stat, sys, datetime, subprocess

class Recording:
    """ Defines everything you need to know to schedule a record """

    def __init__(self, starttime=None, recordpath=None, frequency=0,
            length=0, startearly=40, logfilepath='log.txt', gain=50,
            include='include/'):
        self.starttime  = datetime.datetime.strptime(starttime, "%m/%d/%Y %H:%M")
        self.recordpath = recordpath # ends in Sc16
        self.frequency = float(frequency)
        self.length = int(length)
        self.startearly = int(startearly)
        self.logfilepath = logfilepath
        self.gain = int(gain)
        self.include = include

class Session:

    def __init__(self, logpath = 'log.txt', startingpath=None, hostname=None):
        self.logpath = logpath
        self.startingpath = startingpath
        self.hostname = hostname
        self.recordingList = []
        
