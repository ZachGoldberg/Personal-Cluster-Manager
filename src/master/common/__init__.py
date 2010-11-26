import sys, os, paramiko, getpass

DEBUG = True

def print_stats():
    from common.database import db
    sys.stderr.write("Commits: %s\n" % db.commit_count)
    sys.stderr.write("Hostname: %s\n" % os.environ.get("PCM_HOSTNAME"))
    sys.stderr.write("Host token: %s\n" % os.environ.get("PCM_HOSTTOKEN"))

def die(msg, code=1):
    sys.stderr.write("%s\n" % msg)
    if DEBUG:
        print_stats()

    sys.exit(code)

def succeed(msg="OK"):
    die(msg, code=0)


def check_tunnel(tunnelport, user, keyfile):
    if not user:
        user=getpass.getuser()

    ssh = paramiko.SSHClient()    
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())


    print user
    try:
        if keyfile:
            ssh.connect("127.0.0.1", username=user, port=tunnelport,
                        key_filename=privatekeyfile)
        else:
            ssh.connect("127.0.0.1", username=user, port=tunnelport)

        print "CONNECTED"
    except:
        print "NOT CONNECTED"
        import traceback
        traceback.print_exc()
        

def identity_file():
    return "/tmp/%s.pcm_identity" % os.getppid()

def lookup_id():
    if os.path.exists(identity_file()):
        f = open(identity_file())
        os.environ['PCM_HOSTNAME'] = f.readline().strip()
        os.environ['PCM_HOSTTOKEN'] = f.readline().strip()
        f.close()

