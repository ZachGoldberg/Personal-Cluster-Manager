from __future__ import with_statement
import os, getpass
from contextlib import contextmanager

from storm.database import create_database
from storm.store import Store


from pcm.common import die

DB_LOC = "/var/lib/kinecktor/db.sqlite3"

class Database(object):
    def __init__(self):
        global DB_LOC
        # Check that the root user DB file exists.
        # if so, great, use it.
        # if not, try and create it
        # if we're not root use a local user db file instead.
        if not os.path.exists(DB_LOC):
            if getpass.getuser() == "root":
                self.__init_db()
            else:
                DB_LOC = "%s/.pcm_data" % os.environ['HOME']
                if not os.path.exists(DB_LOC):
                    self.__init_db()
                else:
                    self.__init_store()
        else:
            self.__init_store()

    def add_host(self, host):
        with self.transaction():
            self.store.add(host)

    @contextmanager
    def transaction(self):
        try:
            yield
            self.store.commit()
            self.commit_count += 1
        except:
            self.store.rollback()
            import traceback
            traceback.print_exc()
            
    def __init_store(self):
        self.db = create_database(
            "sqlite:%s" % DB_LOC)

        self.store = Store(self.db)
        self.commit_count = 0

    def __create_table(self, name, types):
        self.store.execute("CREATE TABLE %s %s" % (name,
                           "( %s )" % ', '.join(types)))

    def __init_db(self):
        try:
            os.mkdir(os.path.dirname(DB_LOC))
        except:
            pass
        
        self.__init_store()
        
        # Let others write to the DB... remember we're assuming
        # that we trust these clients, so this is OK.
        os.chmod(DB_LOC, 0666)
        os.chmod(os.path.dirname(DB_LOC), 0777)
        with self.transaction():
            self.__create_table("host", [
                    "id INTEGER PRIMARY KEY",
                    "name VARCHAR",
                    "uniquetoken VARCHAR"
                    ])
            self.__create_table("availability_record", [
                    "id INTEGER PRIMARY KEY",
                    "hostid INTEGER",
                    "hostip VARCHAR",
                    "hostport INTEGER",
                    "masterip VARCHAR",
                    "masterport INTEGER",
                    "tunnelid INTEGER",
                    "tunnelavailable INTEGER",
                    "timestamp DATETIME"
                    ])
            self.__create_table("tunnel", [
                    "id INTEGER PRIMARY KEY",
                    "port INTEGER",
                    "user VARCHAR",
                    "hostid INTEGER",
                    "keyfile VARCHAR"
                    ])

db = Database()
