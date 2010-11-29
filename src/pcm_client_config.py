#!/usr/bin/python
import getpass, sys, os


if __name__ == '__main__':
    questions = [
        ("masterhost", None, "What is the hostname of the PCM master?"),
        ("masteruser", getpass.getuser(), 
         "What is your username on the PCM master?"),     
        ("masterport", 22, 
         "On what port does PCM run on the PCM master?"),
        ("masterkey", "~/.ssh/id_rsa",
         "What SSH Private Key on the local machine can we use to"
         "login to the PCM master?"),
        ("localuser", getpass.getuser(), 
         "What username can the PCM master use to login to "
         "this local machine?"),
        ("localport", 22, 
         "On what port does SSH run on the local machine?"), 
        ("localkey", "~/.ssh/id_rsa",
         "What keyfile (on the master machine!) can be used to login "
         "to the local machine?  (if none exists one must be put there)")
        ]
    
    data = {}
    for question in questions:
        sys.stdout.write("%s [default: %s]: " % (question[2], question[1]))
        sys.stdout.flush()
        data[question[0]] = raw_input()
        if not data[question[0]]:
            data[question[0]] = question[1]

    print data
    output = '\n'.join(["%s=%s" % (k, v) for k, v in data.items()])
    print "Storing config: \n%s" % output
    f = open("%s/.pcm_client_config" % os.environ['HOME'], 'w')
    f.write(output)
    f.close()
