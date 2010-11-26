from common.database import db
from models import Host

def listhosts(args):
    hosts = list(db.store.find(Host))
    for host in hosts:
        print host
