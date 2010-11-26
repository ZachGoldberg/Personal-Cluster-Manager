import os
from datetime import datetime
from storm.locals import *

from common.database import db

class AvailabilityRecord(object):
    __storm_table__ = "availability_record"
    id = Int(primary=True)
    hostid = Int()
    hostip = Unicode()
    hostport = Int()
    masterip = Unicode()
    masterport = Int()
    tunnelid = Int()
    tunnelavailable = Int()
    timestamp = DateTime()
    
    def __init__(self, host, hostip, hostport,
                 masterip, masterport, 
                 tunnelid, tunnelavailable, timestamp):

        self.hostid = host.id
        self.hostip = unicode(hostip)
        self.hostport = int(hostport)
        self.masterip = unicode(masterip)
        self.masterport = int(masterport)
        self.tunnelid = int(tunnelid)
        self.tunnelavailable = int(tunnelavailable)
        self.timestamp = timestamp

        AvailabilityRecord.add_record(self)

    @classmethod
    def add_record(clazz, record):
        with db.transaction():
            db.store.add(record)

    @classmethod
    def register(clazz, host, tunnel):
        tunnel.check_available()

        (hostip, hostport, masterip, masterport) = \
            os.environ['SSH_CONNECTION'].split(' ')
        record = AvailabilityRecord(host,
                                    hostip,
                                    hostport,
                                    masterip,
                                    masterport,
                                    tunnel.id,
                                    tunnel.available,
                                    datetime.now())
        
