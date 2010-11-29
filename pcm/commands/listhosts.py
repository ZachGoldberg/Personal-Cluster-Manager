from pcm.common.database import db
from pcm.models import Host

def listhosts(args):
    hosts = list(db.store.find(Host))
    for host in hosts:
        print host
