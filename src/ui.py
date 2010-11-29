#!/usr/bin/python
import curses, subprocess, os, simplejson
from datetime import datetime

from common.menu import MenuFactory, MenuOption

# NOTES:
# The UI really should *never* be tied to any kind of legwork,
# like refreshing the backend etc.  It should be a dumb client
# ontop of the backend.  On initial load we shouldnt need to
# tell the backend to refresh, we should have a cronjob or a daemon
# which does that for us so we can assume the data we get is recent.


CURRENT_LOC="mainmenu"
AUX = None
SCR = None
HOSTS = []
AVAILABLE = []
YPOS = 0
REFRESH_PROC = None
MENUFACTORY = None


def add_line(str):
    global YPOS
    SCR.addstr(YPOS, 0, str)
    YPOS += 1

def refresh():
    global YPOS
    SCR.clear()
    SCR.refresh()
    YPOS = 0

def refresh_hosts():
    global REFRESH_PROC
    args = "./master.py refresh_tunnels"
    REFRESH_PROC = subprocess.Popen(args, shell=True,
                                    stdout=subprocess.PIPE)
def listhosts():
    menu = MENUFACTORY.new_menu("Known Hosts")
    menu.add_option_vals("Main Menu",
                    action=lambda: change_menu('mainmenu'), hotkey="*")
    for host in HOSTS.values():
        menu.add_option_vals("%s (%s)" % (host['name'], host['uniquetoken']),
                        action=lambda: change_menu('host_options', host))

    menu.render(SCR, add_line)

def showtunnels():
    host = AUX

def showrecords():
    host = AUX

def host_options():
    host = AUX

    menu = MENUFACTORY.new_menu("%s (%s)" % (host['name'], host['uniquetoken']))
    menu.add_option_vals("Main Menu",
                    action=lambda: change_menu('mainmenu'), hotkey="*")
    menu.add_option_vals("Show all associated tunnels",
                    action=lambda: change_menu('showtunnels',  host))
    menu.add_option_vals("Show all associated tunnel activity", 
                    action=lambda: change_menu('showrecords', host))
                    
    menu.render(SCR, add_line)
    

def listtunnels():
    menu = MENUFACTORY.new_menu("Known Tunnels")
    menu.add_option_vals("Main Menu",
                    action= lambda: change_menu('mainmenu'), hotkey="*")
    for host in HOSTS.values():
        menu.add_option_vals("%s (%s)" % (host['name'], host['uniquetoken']),
                        action=lambda: change_menu('host_options', host))

    menu.render(SCR, add_line)


def listrecords():
    pass

def change_menu(newmenu, aux=None):
    global CURRENT_LOC, AUX
    CURRENT_LOC = newmenu
    AUX = aux

def mainmenu():
    menu = MENUFACTORY.new_menu("Main Menu")
    menu.add_option_vals("Refresh Window", action=dir, hotkey="*")
    menu.add_option_vals("List All Known Hosts", 
                    action=lambda: change_menu('listhosts'))
    menu.add_option_vals("List All Known Tunnels", 
                    action=lambda: change_menu('listtunnels'))
    menu.add_option_vals("List All Known Availability Records",
                    action=lambda: change_menu('listrecords'))

    menu.add_option_vals("Refresh Active Hosts", action=refresh_hosts)
#    raise Exception(str(menu))
    menu.render(SCR, add_line)
    
def header():
    add_line("#" * 50)
    add_line("Personal Cluster Management Tool -- Curses UI %s" % datetime.now())
    add_line("#" * 50)

class MenuChanger(object):
    def __init__(self, changer, *args):
        self.changer = changer
        self.args = args

    def __call__(self):
        self.changer(*self.args)

def basic_data():    
    global REFRESH_PROC, AVAILABLE, MENUFACTORY
    add_line("-" * 50)
    if REFRESH_PROC:
        if REFRESH_PROC.poll() != None:
            REFRESH_PROC = None
            AVAILABLE = runcmd("listrecords available unique")            
        else:
            add_line("Refresh Process Running")
            add_line("-" * 50)


    MENUFACTORY = MenuFactory()
    printed = {}
    lines = []
    for host in AVAILABLE:
        if printed.get(host['hostid']):
            continue

        hostobj = HOSTS[int(host['hostid'])]

        lines.append("%s:%s(%s) at %s" % (hostobj['name'],
                                          host['tunnelport'],
                                          hostobj['uniquetoken'],
                                          host['timestamp']))

        option = MenuOption(
            HOSTS[int(host['hostid'])],
            action=(MenuChanger(change_menu, 'host_options', 
                                hostobj)),
            hotkey=str(len(lines)),
            hidden=True)

        MENUFACTORY.add_default_option(option)
        printed[host['hostid']] = True

    add_line("Available Hosts:")
    for num, l in enumerate(lines):
        add_line("%s. %s" % ((num+1), l))

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
