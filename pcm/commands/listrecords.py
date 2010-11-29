from storm.expr import Desc

from pcm.common.database import db
from pcm.models import AvailabilityRecord

def listrecords(args):
    records = list(db.store.find(
            AvailabilityRecord).
                   order_by(Desc(AvailabilityRecord.timestamp)))

    only_available = "available" in args
    unique = "unique" in args

    if not unique:
        for record in records:
            if only_available and record.tunnelavailable == 1:
                print record
            elif only_available == False:
                print record
        return

    
    seenhosts = {}
    for record in records:
        if record.tunnelid in seenhosts:
            continue

        seenhosts[record.tunnelid] = True
        if only_available and record.tunnelavailable == 1:
            print record
        elif only_available == False:
            print record
