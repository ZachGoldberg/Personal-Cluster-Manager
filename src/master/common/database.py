import os, getpass
from contextlib import contextmanager
from storm.locals import *

from common import die

DB_LOC = "/var/lib/kinecktor/db.sqlite3"

class Database(object):
    def __init__(self):
        # Check that the DB file exists.
        # If so, great.
        # If not, try and create it as root.  If we're not root, bail out.
        if not os.path.exists(DB_LOC):
            if getpass.getuser() != "root":
                die("Must be root the first time you run this app")

            self.__init_db()
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
        with self.transaction():
            self.__create_table("host", [
                    "id INTEGER PRIMARY KEY",
                    "name VARCHAR",
                    "uniquetoken VARCHAR"
                    ])

db = Database()
