
class MenuOption(object):
    def __init__(self, value, action, hotkey=None):
        self.value = value
        self.action = action
        self.hotkey = hotkey

class Menu(object):
    def __init__(self, name):
        self.name = name
        self.options = []
        
    def add_option(self, value, action, hotkey=None):
        self.options.append(MenuOption(value, action, hotkey))

    def render(self, screen, writer):
        writer(" " * 20 + self.name)
        hotkeys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                   'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z']
        hotkeys.reverse()
        for option in self.options:
            if not option.hotkey:
                option.hotkey = hotkeys.pop()
            writer("%s. %s" % (option.hotkey, option.value))
        writer("Your Choice: ")
        screen.refresh()
        char = screen.getstr()
        for option in self.options:
            if str(char) == str(option.hotkey):
                return option.action()

        # We didn't match any of the main options, now try a wildcard
        for option in self.options:
            if char == '*':
                return option.action()
