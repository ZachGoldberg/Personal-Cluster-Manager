import sys

def die(msg):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

def succeed(msg):
    print msg
    sys.exit(0)
