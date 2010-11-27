import sys, os

DEBUG = False

def print_stats():
    from common.database import db
    sys.stderr.write("Commits: %s\n" % db.commit_count)
    sys.stderr.write("Hostname: %s\n" % os.environ.get("PCM_HOSTNAME"))
    sys.stderr.write("Host token: %s\n" % os.environ.get("PCM_HOSTTOKEN"))

def die(msg, code=1):
    if msg:
        sys.stderr.write("%s\n" % msg)
    if DEBUG:
        print_stats()

    sys.exit(code)

def succeed(msg=""):
    die(msg, code=0)


def identity_file():
    return "/tmp/%s.pcm_identity" % os.getppid()

def lookup_id():
    if os.path.exists(identity_file()):
        f = open(identity_file())
        os.environ['PCM_HOSTNAME'] = f.readline().strip()
        os.environ['PCM_HOSTTOKEN'] = f.readline().strip()
        f.close()

