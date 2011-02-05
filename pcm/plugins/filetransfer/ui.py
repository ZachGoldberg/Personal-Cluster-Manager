from pcm.common.plugin import UIPlugin
import curses, os

class FileTransferUI(UIPlugin):
    def register_main_menu(self, menu):
        pass

    def fetch_data(self):
        pass

    def copy_to_local(self):
        AVAILABLE = self.data['AVAILABLE']
        TUNNELS = self.data['TUNNELS']

        for record in AVAILABLE:
            if str(record['hostid']) == str(self.host['id']):
                tunnel = TUNNELS[int(record['tunnelid'])]
                break
        
        cmd = "rsync -a -p --progress -e 'ssh -i %s -p %s' %s@localhost:/tmp/pcm /tmp/pcm/" % (
            tunnel['keyfile'],
            tunnel['port'],
            tunnel['user'])


        curses.endwin()
        os.system("clear")
        echo = "Executing copy command: %s" % cmd
        os.system("echo '%s' && %s" % (echo, cmd))
        print "Press enter to continue"
        _ = raw_input()
        self.change_menu('host_options', self.host)


    def register_host_menu(self, menu, host):
        self.host = host
        menu.add_option_vals(
            "Copy remote /tmp/pcm to local /tmp/pcm",
            action=lambda: self.copy_to_local()
            )
