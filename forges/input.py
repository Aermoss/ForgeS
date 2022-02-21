import sdl2

from forges.math import Vector2
from forges.error import ForgeError

class Input:
    def __init__(self):
        self.key = sdl2.SDL_GetKeyboardState(None)
        self.mpos = Vector2(0, 0)

    def update(self, event):
        if event.type == sdl2.SDL_MOUSEMOTION:
            self.mpos.x, self.mpos.y = event.motion.x, event.motion.y

    def key_pressed(self, key):
        return self.key[key]

    def mouse_pos(self):
        return self.mpos