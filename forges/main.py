import sdl2

import os

class ForgeS:
    def __init__(self, parent = None):
        self.windows = []
        self.current_window = None
        self.destroyed = False
        self.enabled = True

        self.parent = parent

        if self.parent != None:
            self.set_parent(parent)

        self.path = self.path = os.path.dirname(os.path.abspath(__file__))
        self.objects = {}
        self.functions = {}
        self.scripts = []
        self.childs = []
    
    def add_window(self, window):
        self.windows.append(window)
        self.current_window = window
        self.objects[self.current_window] = {}

    def get_window(self):
        return self.current_window

    def get_windows(self):
        return self.windows

    def run(self):
        event = sdl2.SDL_Event()

        while not self.destroyed:
            while sdl2.SDL_PollEvent(event) != 0:
                for i in self.windows:
                    self.current_window = i
                    i.event_handler(event)

                if "on_event" in self.functions:
                    self.functions["on_event"](event)

            for i in self.windows:
                self.current_window = i
                i.update_handler()

            if self.enabled:
                self.update()

            if len(self.windows) == 0:
                self.destroy()

            for script in self.scripts:
                if script.enabled:
                    script.update(self.window, self)

    def destroy(self):
        for i in self.childs:
            i.destroy()

        self.destroyed = True
        sdl2.SDL_Quit()

    def bound(self, func):
        setattr(self.__class__, func.__name__, classmethod(func))

    def add_script(self, script):
        self.scripts.append(script)

    def get_script(self, index):
        return self.scripts[index]

    def remove_script(self, script):
        self.scripts.pop(self.scripts.index(script))

    def event(self, func):
        self.functions[func.__name__] = func

    def enable(self, scripts = True):
        for i in self.childs:
            i.enable()

        if scripts:
            for script in self.scripts:
                script.enable()

        self.enabled = True

    def disable(self, scripts = True):
        for i in self.childs:
            i.disable()

        if scripts:
            for script in self.scripts:
                script.disable()

        self.enabled = False

    def update(self):
        pass