#!/usr/bin/python

import sys, subprocess, random, os, time, socket

from common import check_output

masterexec = "~/bin/python ~/pcm/src/master.py"

def get_key():
    return check_output("ifconfig | grep HWaddr | md5sum")[:-2]

def get_tunnel_port(keyfile, masterport, masteruser, masterhost):
    file = "%s/.pcm_tunnel_port" % os.environ['HOME']
    tmptunnelport = None
    if os.path.exists(file):
        try:
            tmptunnelport =  int(open(file).read().strip())            
        except:
            pass

    tunnelport = None
    while not tunnelport:
        # Pick a random tunnel port between 20,000-30,000
        if tmptunnelport:
            tunnelport = tmptunnelport
            tmptunnelport = None
        else:
            tunnelport = 20000 + int(10000*random.random())
        print "Testing port %s" % tunnelport
        data = check_output(
            "ssh %s -p %s %s@%s 'netstat -lnp 2>/dev/null| grep %s'" % (
                keyfile,
                masterport,
                masteruser,
                masterhost,
                tunnelport
                ))

        if data:
            tunnelport = None

    #Cache the tunnel, so we reuse the same port and minimze the need
    #to log about new tunnels
    fd = open(file, 'w')
    fd.write(str(tunnelport))
    fd.close()

    return tunnelport


def main(args):
    masteruser = args[0]
    masterhost = args[1]
    masterport = args[2]
    localport = args[3]
    keyfile = ""
    if len(args) == 5:
        if args[4]:
            keyfile = "-i %s" % args[4]

    uniquekey = get_key()
    tunnelport = get_tunnel_port(keyfile, masterport, masteruser, masterhost)

    print "Got Key: %s\nGot Port: %s" % (uniquekey, tunnelport)

    while True:
        sshcmd = "ssh %s -R %s:localhost:%s -p %s %s@%s" % (
                keyfile,
                tunnelport,
                localport,
                masterport,
                masteruser,
                masterhost
                )
        execmd = "%(exec)s identify %(host)s %(key)s %(tunnel)s %(localuser)s %(localkey)s" % {
            'exec': masterexec,
            'host': socket.gethostname(),
            'key': uniquekey,
            'tunnel': tunnelport,
            'localuser': "zgoldberg",
            'localkey': "",
            }
        cmd = "%s '%s'" % (sshcmd, execmd)
        print "Identifying to master"
        print cmd
        os.system(cmd)
        sshcmd = "%s -N" % sshcmd
        os.system(sshcmd)
        time.sleep(5)

if __name__ == "__main__":

    args = sys.argv
    if len(args) < 4:
        die("Usage: %s masteruser masterhost masterport localport [masterkey]" % args[0])

    main(args[1:])
    
