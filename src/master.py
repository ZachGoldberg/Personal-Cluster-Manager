#!/usr/bin/python

import sys
from common import *
from common.database import db

def check_deps():
    try:
        import storm
    except:
        die("You need python-storm (the ORM) for this application!")

    try:
        import paramiko
    except:
        die("You need python-paramiko (the sshv2 implementation) for this application!")

if __name__ == "__main__":
    check_deps()

    args = sys.argv
    if len(args) < 2:
        die("Usage: %s command commandargs" % args[0])

    lookup_id()
    command = args[1]
    try:
        module = __import__("commands.%s" % command,
                            globals(), locals(), 
                            command)
    except ImportError:
        die("Invalid command: %s" % command)

    module.__dict__[command](args[2:])

    succeed()
