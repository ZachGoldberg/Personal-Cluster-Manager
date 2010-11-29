#!/usr/bin/python
import curses, subprocess, os, simplejson
from datetime import datetime

from pcm.common.menu import MenuFactory, MenuOption

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
TUNNELS = []
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
    args = "pcm_master refresh_tunnels"
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
    menu = MENUFACTORY.new_menu("Known Tunnels for %s" % host['name'])
    menu.add_option_vals("Main Menu",
                    action= lambda: change_menu('mainmenu'), hotkey="*")

    build_tunnel_menu(
        menu,
        [t for t in TUNNELS.values() if t['hostid'] == host['id']])

    menu.render(SCR, add_line)

    
def showrecords():
    host = AUX
    menu = MENUFACTORY.new_menu("Availability Records for %s" % host['name'])
    menu.add_option_vals("Main Menu",
                    action= lambda: change_menu('mainmenu'), hotkey="*")

    build_record_menu(
        menu,
        [r for r in ALL_AVAILABLE if str(r['hostid']) == str(host['id'])])
    
    menu.render(SCR, add_line)


def login():
    global SCR
    host = AUX
    
    for record in AVAILABLE:
        if str(record['hostid']) == str(host['id']):
            tunnel = TUNNELS[int(record['tunnelid'])]
            break
        
    cmd = "ssh -p %s -i %s %s@localhost" % (
        tunnel['port'],
        tunnel['keyfile'],
        tunnel['user'])

    curses.endwin()
    os.system("clear")
    echo = "Executing login command: %s" % cmd
    os.system("echo '%s' && %s" % (echo, cmd))
    change_menu('host_options', host)

def host_options():
    host = AUX

    active = False
    for record in AVAILABLE:
        if str(record['hostid']) == str(host['id']):
            active = True
            break

    avail = "(Down)"
    if active:
        avail = "(Up)"

    menu = MENUFACTORY.new_menu("%s (%s) %s" % (
            host['name'], host['uniquetoken'],
            avail))

    menu.add_option_vals("Main Menu",
                    action=lambda: change_menu('mainmenu'), hotkey="*")

    if active:
        menu.add_option_vals("Login to this machine", 
                             action=lambda: change_menu('login', host))

    menu.add_option_vals("Show all associated tunnels",
                    action=lambda: change_menu('showtunnels',  host))
    menu.add_option_vals("Show all associated tunnel activity", 
                    action=lambda: change_menu('showrecords', host))
                    
    menu.render(SCR, add_line)

def build_tunnel_menu(menu, tunnels):
    for tunnel in tunnels:
        host = HOSTS[tunnel['hostid']]
        menu.add_option_vals("%s: %s:%s (%s)" % (               
                tunnel['hostid'],
                host['name'],
                tunnel['port'],
                tunnel['keyfile']
                ),
                        action=lambda: change_menu('tunnel_options', host))
    

def build_record_menu(menu, records):
    for record in records:
        updown = "Up"
        if record['tunnelavailable'] == "0":
            updown = "Down"

        tunnel = TUNNELS[int(record['hostid'])]
        value =  "%s -R %s %s, %s, %s" % (
            record['hostip'],
            tunnel['port'],
            tunnel['keyfile'],
            updown,
            record['timestamp']
            )
        
        menu.add_option_vals(value,
                        action=lambda: change_menu('showrecords', host),
                        hotkey="-")

def listtunnels():
    menu = MENUFACTORY.new_menu("Known Tunnels")
    menu.add_option_vals("Main Menu",
                    action= lambda: change_menu('mainmenu'), hotkey="*")

    build_tunnel_menu(menu, TUNNELS.values())

    menu.render(SCR, add_line)

def listrecords():
    menu = MENUFACTORY.new_menu("Availability Records")
    menu.add_option_vals("Main Menu",
                    action= lambda: change_menu('mainmenu'), hotkey="*")

    build_record_menu(menu, ALL_AVAILABLE)

    menu.render(SCR, add_line)


def show_tunnel_usage():
    tunnel = AUX
    menu = MENUFACTORY.new_menu("Tunnel Usage")
    menu.add_option_vals("Main Menu",
                    action= lambda: change_menu('mainmenu'), hotkey="*")
    
    build_record_menu(
        menu,
        [r for r in ALL_AVAILABLE if str(r['tunnelid']) == str(tunnel['id'])])

    menu.render(SCR, add_line)
        

def tunnel_options():
    tunnel = AUX
    menu = MENUFACTORY.new_menu("Tunnel Options")
    menu.add_option_vals("Main Menu",
                    action= lambda: change_menu('mainmenu'), hotkey="*")
    menu.add_option_vals(
        "Show Tunnel Usage",
        action=lambda: change_menu('show_tunnel_usage', tunnel))
        
    menu.render(SCR, add_line)


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
        if printed.get(host['tunnelid']):
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
        printed[host['tunnelid']] = True

    add_line("Available Hosts:")
    for num, l in enumerate(lines):
        add_line("%s. %s" % ((num+1), l))

    add_line("-" * 50)


def runcmd(args, parse=True):
    os.environ['PCM_AS_JSON'] = "True"
    args = "pcm_master %s" % args
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

def loadtunnels():
    global TUNNELS
    tunnellist = runcmd("listtunnels")
    TUNNELS = {}
    for tunnel in tunnellist:
        TUNNELS[tunnel['id']]= tunnel

def refresh_data():
    add_line("Loading host data...")
    SCR.refresh()
    loadhosts()

    add_line("Loading tunnel data...")
    SCR.refresh()
    loadtunnels()

    add_line("Refreshing available records...")
    SCR.refresh()
    global AVAILABLE
    AVAILABLE = runcmd("listrecords available unique")

    add_line("Refreshing records...")
    SCR.refresh()
    global ALL_AVAILABLE
    ALL_AVAILABLE = runcmd("listrecords")


def main():    
    global SCR, HOSTS, AVAILABLE
    SCR = curses.initscr()
    refresh()

    SCR.timeout(5000)

    refresh_data()
    
    while True:
        refresh()
        header()
        basic_data()
        globals()[CURRENT_LOC]()

    curses.endwin()

def run():
    try:
        main()
    except:
        curses.endwin()


if __name__ == '__main__':
    run()
