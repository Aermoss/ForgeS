from forges.script import *

class ToggleFullscreen(Script):
    def __init__(self):
        super().__init__()

        self.state = False

    def update(self, window, entity):
        if not window.fullscreen:
            self.bwidth, self.bheight = window.get_width(), window.get_height()

        if window.input.key_pressed(window.keys["F11"]):
            if self.state:
                self.state = False

                if window.fullscreen:
                    window.width, window.height = self.bwidth, self.bheight
                    window.set_fullscreen(False)
                    window.set_size(self.bwidth, self.bheight)

                else:
                    self.mwidth, self.mheight = window.get_monitor_size()
                    window.set_size(self.mwidth, self.mheight)
                    window.set_fullscreen(True)

        else:
            self.state = True