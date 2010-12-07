from pcm.plugins.screen.ui import ScreenUI
from pcm.plugins.screen.backend import ScreenBackend

UI_PLUGINS = [
    ScreenUI
    ]

BACKEND_PLUGINS = [
    ScreenBackend
    ]

PLUGINS = []
BK_PLUGINS = []

def init_plugins(plugindata):
    global PLUGINS
    for cls in UI_PLUGINS:
        PLUGINS.append(cls(plugindata.get(str(cls), None)))
        
    for cls in BACKEND_PLUGINS:
        BK_PLUGINS.append(cls(plugindata.get(str(cls), None)))


def plugin_main_menu_options(menu):
    [plugin.register_main_menu(menu) for plugin in PLUGINS]

if __name__ == '__main__':
    init_plugins({})
    
