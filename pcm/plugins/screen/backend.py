from storm.locals import *

from pcm.common.plugin import BackendPlugin

class ScreenSession(Storm):
    __storm_table__ = "screensession"

    id = Int(primary=True)
    hostid = Int()
    host = Reference(hostid, "Host.id")
    screenid = Unicode()
    active = Int()

    def __str__(self):
        if os.environ.get('PCM_AS_JSON'):
            values = ["id", "hostid", "screenid", "active"]
            data = dict(zip(values, [str(getattr(self, v)) for v in values]))
            return simplejson.dumps(data)
                
        return "%s, %s, %s" % (
            self.hostid,
            self.screenid,
            self.active
            )

class ScreenBackend(BackendPlugin):

    def listscreens(self, args):
        from pcm.common.database import db        
        screens = list(db.store.find(ScreenSession))
        print screens

    def create_tables(self, db):
        db._create_table("screensession", [
                    "id INTEGER PRIMARY KEY",
                    "hostid INTEGER",
                    "screenid VARCHAR",
                    "active INTEGER",
                    ])
        
    def get_commands(self):
        return {'listscreens': self.listscreens}


    def fetch_data(self):
        pass
