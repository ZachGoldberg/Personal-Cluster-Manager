from __future__ import with_statement
import os, simplejson
from storm.properties import *

from pcm.common.database import db

class Host(object):
    __storm_table__ = "host"
    id = Int(primary=True)
    name = Unicode()
    uniquetoken = Unicode()
    def __init__(self, name, uniquetoken):
        self.name = unicode(name)
        self.uniquetoken = unicode(uniquetoken)
        Host.add_host(self)
           
    def __str__(self):
        if os.environ.get('PCM_AS_JSON'):
            return simplejson.dumps({
                    'name': self.name,
                    'id': self.id,
                    'uniquetoken': self.uniquetoken
                    })
        return "%s (%s)" % (self.name, self.uniquetoken)
        
    @classmethod
    def add_host(clazz, host):
        with db.transaction():
            db.store.add(host)
            
    @classmethod
    def find_host(clazz, hostname, hostid):
        result = db.store.find(Host,
                               Host.name == hostname,
                               Host.uniquetoken == hostid).one()
        return result
