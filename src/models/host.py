from storm.locals import *

from common.database import db

class Host(object):
    __storm_table__ = "host"
    id = Int(primary=True)
    name = Unicode()
    uniquetoken = Unicode()
    def __init__(self, name, uniquetoken):
        self.name = unicode(name)
        self.uniquetoken = unicode(uniquetoken)
        Host.add_host(self)
           
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
