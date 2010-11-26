
import sys

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print "Usage: %s command commandargs" % args[0]
        sys.exit(1)

