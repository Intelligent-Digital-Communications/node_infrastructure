import os, shutil, stat, sys, datetime, subprocess, json

class Recording:
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

    def _json(self):
        return json.dumps(_jsoncleandict())

    def _jsoncleandict(self):
        datetimeholder = self.starttime
        tempdict = dict(self.__dict__)
        tempdict['starttime'] = self.starttime.isoformat()
        tempdict['__type__'] = 'Recording'
        return tempdict

    def __str__(self):
        return '{} {}'.format(self.recordpath, self.starttime.isoformat())

class Session:
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

    def _json(self):
        returning = dict(self.__dict__)
        returning['__type__'] = 'Session'
        returning['recordings'] = [x._jsoncleandict() for x in self.recordings]
        return json.dumps(returning)

    def __str__(self):
        return '{} {}'.format(self.name, str(self.recordings))


class IDCJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj._json()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)

class IDCJSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        print('HEY ma')
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            inst = class_(**args)
        else:
            inst = d
        return inst
