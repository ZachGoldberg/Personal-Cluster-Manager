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
        db.add_host(self)
        
