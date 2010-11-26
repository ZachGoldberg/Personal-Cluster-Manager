from common.database import db
from models import Tunnel

def listtunnels(args):
    tunnels = list(db.store.find(Tunnel))
    for tunnel in tunnels:
        print tunnel
