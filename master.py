


class ConnectionListener(object):
    pass


class Master(ConnectionListener):
    def __init__(self):
        pass

    
    """
    Protocol Definition:
    Initial Client Connection:
      Client Self Identification (including key, hostname)
      Server verifies that its an existing node, comparing key
      to a verified database.
      
    """

    def recieveConnection(self, clientName):

