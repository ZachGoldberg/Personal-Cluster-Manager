import curses

from models import *
from common.database import db

if __name__ == '__main__':


    print [str(i) for i in list(db.store.find(Host))]
    print [str(i) for i in list(db.store.find(Tunnel))]
    print [str(i) for i in list(db.store.find(AvailabilityRecord))]
