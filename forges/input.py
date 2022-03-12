import sdl2

from forges.math import Vector2
from forges.error import ForgeError

class Input:
    def __init__(self, window):
        self.window = window

        self.key = sdl2.SDL_GetKeyboardState(None)
        self.kpressed = None

        self.mbutton = {sdl2.SDL_BUTTON_LEFT: False, sdl2.SDL_BUTTON_MIDDLE: False, sdl2.SDL_BUTTON_RIGHT: False}
        self.mpos = Vector2(0, 0)
        self.last_mpos = self.mpos.copy()
        self.mwheel = 0
        self.mmotion = False

    def update(self, event):
        self.mmotion = False

        if event.type == sdl2.SDL_MOUSEMOTION:
            self.last_mpos = self.mpos.copy()
            self.mpos.x, self.mpos.y = event.motion.x, event.motion.y
            self.mmotion = True

        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            self.mpos.x, self.mpos.y = event.button.x, event.button.y
            self.mbutton[event.button.button] = True

        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            self.mpos.x, self.mpos.y = event.button.x, event.button.y
            self.mbutton[event.button.button] = False

        elif event.type == sdl2.SDL_MOUSEWHEEL:
            self.mwheel = event.wheel.y

        elif event.type == sdl2.SDL_KEYDOWN:
            self.kpressed = sdl2.SDL_GetKeyName(sdl2.SDL_GetKeyFromScancode(event.key.keysym.scancode)).decode()

        elif event.type == sdl2.SDL_KEYUP:
            self.kpressed = None

    def key_pressed(self, key = None):
        if key != None:
            if self.key[key]:
                return True

        else:
            for i in self.window.keys:
                if self.key[self.window.keys[i]]:
                    return True

        return False

    def get_keyname(self, reset = False):
        temp = self.kpressed

        if reset:
            self.kpressed = None

        return temp

    def mouse_pressed(self, button = None):
        if button != None:
            return self.mbutton[button]

        else:
            for i in self.window.buttons:
                if self.mbutton[self.window.buttons[i]]:
                    return True

        return False

    def mouse_pos(self):
        return self.mpos

    def mouse_rel(self):
        temp = self.last_mpos - self.mpos
        self.last_mpos = self.mpos.copy()
        return temp

    def mouse_motion(self):
        temp = self.mmotion
        self.mmotion = False
        return temp

    def mouse_wheel(self):
        temp = self.mwheel
        self.mwheel = 0
        return temp