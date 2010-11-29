from pcm.common.database import db
from pcm.models import Tunnel

def listtunnels(args):
    tunnels = list(db.store.find(Tunnel))
    for tunnel in tunnels:
        print tunnel
