from common.database import db
from models import AvailabilityRecord

def listrecords(args):
    records = list(db.store.find(AvailabilityRecord))
    for record in records:
        print record
