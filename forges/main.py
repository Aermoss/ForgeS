import sdl2

import os

class ForgeS:
    def __init__(self):
        self.window = None
        self.destroyed = False

        self.path = self.path = os.path.dirname(os.path.abspath(__file__))
        self.objects = {}
    
    def set_window(self, window):
        self.window = window

    def get_window(self):
        return self.window

    def run(self):
        event = sdl2.SDL_Event()

        while not self.destroyed:
            while sdl2.SDL_PollEvent(event) != 0:
                self.window.event_handler(event)

            self.window.update_handler()

    def destroy(self):
        self.destroyed = True