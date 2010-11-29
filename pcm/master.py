#!/usr/bin/python

import sys
from pcm.common import *
from pcm.common.database import db


def check_deps():
    try:
        import storm
    except:
        die("You need python-storm (the ORM) for this application!")

    try:
        import paramiko
    except:
        die("You need python-paramiko (the sshv2 implementation) for this application!")

    try:
        import simplejson
    except:
        die("You need python-simplejson for this application!")

    try:
        import threadpool
    except:
        die("You need python-threadpool for this application!")

def run():
    check_deps()

    args = sys.argv
    if len(args) < 2:
        die("Usage: %s command commandargs" % args[0])

    lookup_id()
    command = args[1]
    try:
        module = __import__("pcm.commands.%s" % command,
                            globals(), locals(), 
                            command)
    except ImportError:
        die("Invalid command: %s" % command)
        import traceback
        traceback.print_exc()
        

    module.__dict__[command](args[2:])

    succeed()


if __name__ == "__main__":
    run()
