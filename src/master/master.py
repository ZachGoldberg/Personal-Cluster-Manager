import sys
from common.database import db
from common import *

if __name__ == "__main__":
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
