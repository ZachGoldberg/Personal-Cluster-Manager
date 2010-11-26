import os, simplejson
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
    tunnel = None

    def __init__(self, host, hostip, hostport,
                 masterip, masterport, 
                 tunnelid, tunnelavailable, timestamp,
                 tunnel = None):

        self.hostid = host.id
        self.hostip = unicode(hostip)
        self.hostport = int(hostport)
        self.masterip = unicode(masterip)
        self.masterport = int(masterport)
        self.tunnelid = int(tunnelid)
        self.tunnelavailable = int(tunnelavailable)
        self.timestamp = timestamp

        if not tunnel:
            from models import Tunnel
            self.tunnel = db.store.get(Tunnel, self.tunnelid)
        else:
            self.tunnel = tunnel

        AvailabilityRecord.add_record(self)


    def __str__(self):
        if not self.tunnel:
            from models import Tunnel
            self.tunnel = db.store.get(Tunnel, self.tunnelid)
        if os.environ.get('PCM_AS_JSON'):
            values = ['hostip', 'id', 'hostport', 
                      'masterip', 'masterport',
                      'tunnelavailable', 
                      'timestamp']
            data = dict(zip(values, [str(getattr(self, v)) for v in values]))
            data['tunnelport'] = self.tunnel.port
                       
            return simplejson.dumps(data)
                
        return "%s:%s -> %s:%s -R port %s, Available: %s" % (
            self.hostip,
            self.hostport,
            self.masterip,
            self.masterport,
            self.tunnel.port,
            self.tunnelavailable
            )

    @classmethod
    def add_record(clazz, record):
        with db.transaction():
            db.store.add(record)

    @classmethod
    def register(clazz, host, tunnel):
        tunnel.check_available()

        (hostip, hostport, masterip, masterport) = \
            os.environ['SSH_CONNECTION'].split(' ')
        return AvailabilityRecord(host,
                                  hostip,
                                  hostport,
                                  masterip,
                                  masterport,
                                  tunnel.id,
                                  tunnel.available,
                                  datetime.now(),
                                  tunnel)
        
        
