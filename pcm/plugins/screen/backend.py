from pcm.common.plugin import BackendPlugin

class ScreenBackend(BackendPlugin):

    def showscreens(self, args):
        print args

    def get_commands(self):
        return {'showscreens': self.showscreens}
