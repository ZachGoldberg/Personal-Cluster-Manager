import sys

from common.database import db
from models import Host



def addnode(args):
    if len(args) < 2:
        sys.stderr.write("addnode hostname hostuniqueid\n")
        sys.exit(1)

    host = Host(args[0], args[1])
