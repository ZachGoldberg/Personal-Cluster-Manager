from pcm.common.database import db
from pcm.common import *
from pcm.models import Host



def addnode(args):
    if len(args) < 2:
        die("addnode syntax: addnode <hostname> <hostuniqueid>")
        
    hostname = unicode(args[0])
    hostid = unicode(args[1])
        
    # Check if this host exists, if so bail out
    host = Host.find_host(hostname, hostid)
    if host:
        die("Host already exists")
    else:
        host = Host(args[0], args[1])
        succeed("Host registered")

    return host
