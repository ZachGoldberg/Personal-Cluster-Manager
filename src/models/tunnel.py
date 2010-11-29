from __future__ import with_statement
import getpass, paramiko, simplejson, os
from storm.properties import *

from common.database import db

class Tunnel(object):
    __storm_table__ ="tunnel"
    id = Int(primary=True)
    port = Int()
    user = Unicode()
    keyfile = Unicode()
    hostid = Int()

    def __init__(self, tunnelport, host, user=None, keyfile=None):
        self.port = tunnelport
        self.user = unicode(user) or unicode(getpass.getuser())
        self.user = unicode(self.user)
        self.keyfile = unicode(keyfile)
        self.hostid = host.id
        self.available = -1
        Tunnel.add_tunnel(self)


    def __str__(self):
        if os.environ.get('PCM_AS_JSON'):
            return simplejson.dumps({
                    'user': self.user,
                    'port': self.port,
                    'hostid': self.hostid,
                    'keyfile': self.keyfile,
                    'id': self.id
                    })
        return "%s: %s@localhost:%s (%s)" % (self.hostid,
                                             self.user, self.port, self.keyfile)

    @classmethod
    def get_tunnel(clazz, tunnelport, host, user=None, keyfile=None):
        result = db.store.find(Tunnel,
                               Tunnel.port == tunnelport,
                               Tunnel.user == unicode(user),
                               Tunnel.keyfile == unicode(keyfile),
                               Tunnel.hostid == int(host.id))

        if result.count() == 0:
            return Tunnel(tunnelport, host, user, keyfile)

        return result[0]

    @classmethod
    def add_tunnel(clazz, tunnel):
        with db.transaction():
            db.store.add(tunnel)


    def check_available(self):
        ssh = paramiko.SSHClient()    
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())

        try:
            if self.keyfile:
                ssh.connect("127.0.0.1", username=self.user, port=self.port,
                            key_filename=self.keyfile)
            else:
                ssh.connect("127.0.0.1", username=self.user, port=self.port)
            #TODO: Should confirm that the host we logged into is
            # actually the host we were looking for.
            ssh.close()
            
            self.available = True
        except:
            self.available = False

        return self.available
    
