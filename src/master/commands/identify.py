from common.database import db
from common import *
from models import Host, AvailabilityRecord, Tunnel



def identify(args):
    if len(args) < 3:
        die("identify syntax: identify "
            "<hostname> <hostuniqueid> <tunnelport> [hostuser] [privatekeyfile]")
        
    hostname = unicode(args[0])
    hostid = unicode(args[1])
    tunnelport = int(args[2])
    hostuser = ""
    privatekey = ""

    if len(args) > 3:
        hostuser = unicode(args[3])

    if len(args) > 4:
        privatekey = unicode(args[4])

    host = Host.find_host(hostname, hostid)
    if not host:
        host = Host(args[0], args[1])

    # Write a session ID so we know who this is
    f = open(identity_file(), 'w')
    f.write("%s\n%s" % (hostname, hostid))
    f.close()    

    # Check if the tunnel works
    tunnel = Tunnel.get_tunnel(tunnelport, hostuser, privatekey)

    # Log that we saw this machine
    AvailabilityRecord.register(host, tunnel)
