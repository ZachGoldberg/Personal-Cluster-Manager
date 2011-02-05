from pcm.plugins.screen.ui import ScreenUI
from pcm.plugins.screen.backend import ScreenBackend
from pcm.plugins.filetransfer.ui import FileTransferUI


UI_PLUGINS = [
    ScreenUI,
    FileTransferUI
    ]

BACKEND_PLUGINS = [
    ScreenBackend
    ]

PLUGINS = []
BK_PLUGINS = []
CMDS = {}

def init_plugins(plugindata, change_menu):
    global PLUGINS, BK_PLUGINS
    for cls in UI_PLUGINS:
        PLUGINS.append(cls(plugindata, change_menu))
        
    for cls in BACKEND_PLUGINS:
        BK_PLUGINS.append(cls())


def create_tables(database):
    if not BK_PLUGINS:
        init_plugins({})

    for plugin in BK_PLUGINS:
        plugin.create_tables(database)
    

def get_plugin_command(cmd):
    if not BK_PLUGINS:
        init_plugins({})

    for plugin in BK_PLUGINS:
        cmds = plugin.get_commands()
        if cmd in cmds:
            return cmds[cmd]

def plugin_main_menu_options(menu):
    [plugin.register_main_menu(menu) for plugin in PLUGINS]

def plugin_host_menu_options(menu, host):
    [plugin.register_host_menu(menu, host) for plugin in PLUGINS]

if __name__ == '__main__':
    init_plugins({})
    
