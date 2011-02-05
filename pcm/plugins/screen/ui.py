from pcm.common.plugin import UIPlugin

class ScreenUI(UIPlugin):
    def register_main_menu(self, menu):
        pass

    def fetch_data(self):
        pass

    def register_host_menu(self, menu, host):
        menu.add_option_vals(
            "Show Screen Sessions",
            action=lambda: change_menu('mainmenu')
            )
        
