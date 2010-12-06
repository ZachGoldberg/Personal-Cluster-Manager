class Plugin(object):
    def __init__(self, initialdata):
        """
        Initialize this plugin with the passed in initialdata packet
        """
        self.data = initialdata

    def fetch_data(self):
        """
        Called periodically by the UI to refresh this plugin's
        internal datastructure.
        """
        pass

    def register_main_menu(self, menu):
        """
        Add any options that are needed to the main menu.
        Should NOT include a "refresh data" option, that will
        be handled by the UI and will call back to fetch_data
        """
        pass

    def register_host_menu(self, menu):
        """
        Add any options needed for the menu of a specific machine
        """
        pass
