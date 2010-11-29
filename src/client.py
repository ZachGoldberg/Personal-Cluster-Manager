#!/usr/bin/python

import sys, subprocess, random, os, time, socket, optparse

from common import check_output

masterexec = "pcmmaster"

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


def main(options):
    masteruser = options.masteruser
    masterhost = options.masterhost
    masterport = options.masterport
    localport = options.localport
    keyfile = "-i %s" % options.masterkey

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
            'localuser': options.localuser,
            'localkey': options.localkey,
            }
        cmd = "%s '%s'" % (sshcmd, execmd)
        print "Identifying to master"
        print cmd
        os.system(cmd)
        sshcmd = "%s -N" % sshcmd
        os.system(sshcmd)
        time.sleep(5)

def parse_args():

    parser = optparse.OptionParser()
    parser.add_option('-H', '--master-host', action='store',
                       dest='masterhost',
                       help='Host of the master server')

    parser.add_option('-U', '--master-user', action='store',
                       dest='masteruser',
                       help='Username to login to the master server')

    parser.add_option('-P', '--master-port', action='store',
                      dest='masterport',
                      default='22',
                      help="SSH port on the master server (default: 22)")

    parser.add_option('-K', '--master-key', action='store',
                      dest='masterkey',
                      help="SSH private key to use to login to the master")

    parser.add_option('-u', '--local-user', action='store',
                       dest='localuser',
                       help='Username to login to the client server'
                      'from the master')

    parser.add_option('-p', '--local-port', action='store',
                      dest='localport',
                      default='22',
                      help="SSH port on the client server (default: 22)")

    parser.add_option('-k', '--local-key', action='store',
                      dest='localkey',
                      help="SSH file (on the remote master machine)"
                      "which the master uses to login to the client")
    

    options, _ = parser.parse_args()

    file = "%s/.pcm_client_config" % os.environ['HOME']
    if (os.path.exists(file)):
        data = open(file).read().split('\n')
        for line in data:
            k, v = line.split('=')
            if not getattr(options, k):
                setattr(options, k, v)

    if not options.localuser or not options.masterkey or \
            not options.localkey or not options.masteruser or \
            not options.masterhost:
        parser.error("Missing options.  Please consult --help for a list of"
                     "required options")
    

    return options


if __name__ == "__main__":

    options = parse_args()
    main(options)
    
