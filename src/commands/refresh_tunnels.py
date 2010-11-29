from threadpool import ThreadPool, WorkRequest

from common.database import db
from models import *


def refresh_tunnels(args):
    tunnels = db.store.find(Tunnel)
    if tunnels:
        pool = ThreadPool(tunnels.count())
        for tunnel in tunnels:
            request = WorkRequest(tunnel.check_available)
            pool.putRequest(request)

        pool.wait()
        
    for tunnel in tunnels:
        host = db.store.get(Host, tunnel.hostid)
        record = AvailabilityRecord.register(host, tunnel, check=False)
        print record
