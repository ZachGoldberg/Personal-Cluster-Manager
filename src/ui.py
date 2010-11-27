#!/usr/bin/python
import curses, subprocess, os, simplejson
from datetime import datetime
# NOTES:
# The UI really should *never* be tied to any kind of legwork,
# like refreshing the backend etc.  It should be a dumb client
# ontop of the backend.  On initial load we shouldnt need to
# tell the backend to refresh, we should have a cronjob or a daemon
# which does that for us so we can assume the data we get is recent.


CURRENT_LOC="mainmenu"
SCR = None
HOSTS = []
AVAILABLE = []
YPOS = 0
REFRESH_PROC = None

def add_line(str):
    global YPOS
    SCR.addstr(YPOS, 0, str)
    YPOS += 1

def refresh():
    global YPOS
    SCR.clear()
    SCR.refresh()
    YPOS = 0

def mainmenu():
    add_line(" " * 20 + "Main Menu")
    add_line("_. Refresh Window")
    add_line("a. List All Known Hosts")
    add_line("b. List All Known Tunnels")
    add_line("c. List All Known Availability Records")
    add_line("d. Refresh Active Hosts")
    add_line("Your Choice: ")
    SCR.refresh()
    char = SCR.getstr()
    if char == "d":
        global REFRESH_PROC
        args = "./master.py refresh_tunnels"
        REFRESH_PROC = subprocess.Popen(args, shell=True,
                         stdout=subprocess.PIPE)
        
def header():
    add_line("#" * 50)
    add_line("Personal Cluster Management Tool -- Curses UI %s" % datetime.now())
    add_line("#" * 50)



def basic_data():    
    global REFRESH_PROC, AVAILABLE
    add_line("-" * 50)
    if REFRESH_PROC:
        if REFRESH_PROC.poll() != None:
            REFRESH_PROC = None
            AVAILABLE = runcmd("listrecords available unique")            
        else:
            add_line("Refresh Process Running")
            add_line("-" * 50)

    printed = {}
    lines = []
    for host in AVAILABLE:
        if printed.get(host['hostid']):
            continue

        lines.append("%s:%s at %s" % (HOSTS[int(host['hostid'])]['name'],
                                  host['tunnelport'],
                                  host['timestamp']))
        printed[host['hostid']] = True

    add_line("Available Hosts:")
    [add_line("%s. %s" % ((num+1), l)) for num, l in enumerate(lines)]
    add_line("-" * 50)


def runcmd(args, parse=True):
    os.environ['PCM_AS_JSON'] = "True"
    args = "./master.py %s" % args
    data = subprocess.Popen(args, shell=True,
                            stdout=subprocess.PIPE).communicate()[0].strip()
    if not parse:
        return data

    records = []
    for line in data.split("\n"):
        if line:
            records.append(simplejson.loads(line))
    return records

def loadhosts():
    global HOSTS
    hostlist = runcmd("listhosts")
    HOSTS = {}
    for host in hostlist:
        HOSTS[host['id']] = host

def main():    
    global SCR, HOSTS, AVAILABLE
    SCR = curses.initscr()
    refresh()

    SCR.timeout(5000)

    add_line("Loading initial host data...")
    SCR.refresh()
    loadhosts()

    add_line("Refreshing tunnel state...")
    SCR.refresh()
    runcmd("refresh_tunnels", parse=False)

    add_line("Refreshing available records...")
    SCR.refresh()
    AVAILABLE = runcmd("listrecords available unique")

    while True:
        refresh()
        header()
        basic_data()
        globals()[CURRENT_LOC]()
    curses.endwin()

if __name__ == '__main__':
    try:
        main()
    except:
        curses.endwin()
        import traceback
        traceback.print_exc()
