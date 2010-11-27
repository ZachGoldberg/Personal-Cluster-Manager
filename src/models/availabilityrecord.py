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
            values = ['hostid', 'hostip', 'id', 'hostport', 
                      'masterip', 'masterport',
                      'tunnelavailable', 
                      'tunnelid',
                      'timestamp']
            data = dict(zip(values, [str(getattr(self, v)) for v in values]))
            data['tunnelport'] = self.tunnel.port
                       
            return simplejson.dumps(data)
                
        return "%s:%s -> %s:%s -R port %s (%s), Available: %s" % (
            self.hostip,
            self.hostport,
            self.masterip,
            self.masterport,
            self.tunnel.port,
            self.tunnel.keyfile,
            self.tunnelavailable
            )

    @classmethod
    def add_record(clazz, record):
        with db.transaction():
            db.store.add(record)

    @classmethod
    def register(clazz, host, tunnel, check=True):
        if check:
            tunnel.check_available()
            
        if "SSH_CONNECTION" in os.environ:
            (hostip, hostport, masterip, masterport) = \
                os.environ.get('SSH_CONNECTION').split(' ')
        else:
            hostip = 0
            hostport = 0
            masterip = 0
            masterport = 0
        return AvailabilityRecord(host,
                                  hostip,
                                  hostport,
                                  masterip,
                                  masterport,
                                  tunnel.id,
                                  tunnel.available,
                                  datetime.now(),
                                  tunnel)
        
        
