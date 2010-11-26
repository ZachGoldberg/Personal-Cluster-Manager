import sys

DEBUG = True

def print_stats():
    from common.database import db
    sys.stderr.write("Commits: %s\n" % db.commit_count)

def die(msg, code=1):
    sys.stderr.write("%s\n" % msg)
    if DEBUG:
        print_stats()

    sys.exit(code)

def succeed(msg):
    die(msg, code=0)
