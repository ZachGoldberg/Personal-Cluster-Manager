#!/usr/bin/python
import curses, subprocess, os, simplejson

CURRENT_LOC="mainmenu"
SCR = None
HOSTS = []
AVAILABLE = []
YPOS = 0

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
    add_line("0. Refresh Window")
    add_line("1. List All Known Hosts")
    add_line("2. List All Known Tunnels")
    add_line("3. List All Known Availability Records")
    add_line("4. Refresh Active Hosts")
    add_line("Your Choice: ")
    SCR.refresh()
    SCR.getstr()
    

def header():
    add_line("#" * 50)
    add_line("Personal Cluster Management Tool -- Curses UI")
    add_line("#" * 50)



def basic_data():    
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

    add_line("(%s) Available Hosts:" % len(lines))
    [add_line(l) for l in lines]
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
    add_line("Loading initial data...")
    SCR.refresh()
    
    loadhosts()
    runcmd("refresh_tunnels", parse=False)
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
