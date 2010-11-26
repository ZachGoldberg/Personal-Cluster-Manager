import sys

from common.database import db
from common import *
from models import Host



def addnode(args):
    if len(args) < 2:
        die("addnode syntax: addnode <hostname> <hostuniqueid>")
        
    hostname = unicode(args[0])
    hostid = unicode(args[1])
        
    # Check if this host exists, if so bail out
    if Host.find_host(hostname, hostid):
        die("Host already exists")
    else:
        host = Host(args[0], args[1])
        succeed("Host registered")
