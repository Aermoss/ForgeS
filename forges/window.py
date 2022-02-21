import sdl2
import sdl2.ext

import os
import time

from forges.input import Input
from forges.color import Color

import __main__

class Window:
    def __init__(self, width = 1200, height = 600, vsync = True, background_color = Color(255, 255, 255, 255)):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.engine.set_window(self)

        self.width = width
        self.height = height
        self.vsync = vsync
        self.background_color = background_color

        self.start_time = time.time()
        self.destroyed = False
        self.functions = {}

        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        self.window = sdl2.SDL_CreateWindow("Forge S".encode(), sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, self.width, self.height, sdl2.SDL_WINDOW_SHOWN)
        
        if self.vsync:
            self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)

        else:
            self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, 0)

        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_BLEND)

        self.path = self.engine.path

        icon = self.path + "\\assets\\icon\\icon.png"
        icon = sdl2.ext.load_image(icon)
        sdl2.SDL_SetWindowIcon(self.window, icon)

        self.input = Input()

        self.keys = {
            "ESCAPE" : sdl2.SDL_SCANCODE_ESCAPE,

            "UP": sdl2.SDL_SCANCODE_UP, "DOWN": sdl2.SDL_SCANCODE_DOWN,
            "LEFT": sdl2.SDL_SCANCODE_LEFT, "RIGHT": sdl2.SDL_SCANCODE_RIGHT,

            "A": sdl2.SDL_SCANCODE_A, "B": sdl2.SDL_SCANCODE_B, "C": sdl2.SDL_SCANCODE_C,
            "D": sdl2.SDL_SCANCODE_D, "E": sdl2.SDL_SCANCODE_E, "F": sdl2.SDL_SCANCODE_F,
            "G": sdl2.SDL_SCANCODE_G, "H": sdl2.SDL_SCANCODE_H, "I": sdl2.SDL_SCANCODE_I,
            "J": sdl2.SDL_SCANCODE_J, "K": sdl2.SDL_SCANCODE_K, "L": sdl2.SDL_SCANCODE_L,
            "M": sdl2.SDL_SCANCODE_M, "N": sdl2.SDL_SCANCODE_N, "O": sdl2.SDL_SCANCODE_O,
            "P": sdl2.SDL_SCANCODE_P, "Q": sdl2.SDL_SCANCODE_Q, "R": sdl2.SDL_SCANCODE_R,
            "S": sdl2.SDL_SCANCODE_S, "T": sdl2.SDL_SCANCODE_T, "U": sdl2.SDL_SCANCODE_U,
            "V": sdl2.SDL_SCANCODE_V, "W": sdl2.SDL_SCANCODE_W, "X": sdl2.SDL_SCANCODE_X,
            "Y": sdl2.SDL_SCANCODE_Y, "Z": sdl2.SDL_SCANCODE_Z,
  
            "0": sdl2.SDL_SCANCODE_0, "1": sdl2.SDL_SCANCODE_1,"2": sdl2.SDL_SCANCODE_2, 
            "3": sdl2.SDL_SCANCODE_3, "4": sdl2.SDL_SCANCODE_4, "5": sdl2.SDL_SCANCODE_5,
            "6": sdl2.SDL_SCANCODE_6, "7": sdl2.SDL_SCANCODE_7, "8": sdl2.SDL_SCANCODE_8,
            "9": sdl2.SDL_SCANCODE_9,

            "F1": sdl2.SDL_SCANCODE_F1, "F2": sdl2.SDL_SCANCODE_F2, "F3": sdl2.SDL_SCANCODE_F3,
            "F4": sdl2.SDL_SCANCODE_F4, "F5": sdl2.SDL_SCANCODE_F5, "F6": sdl2.SDL_SCANCODE_F6,
            "F7": sdl2.SDL_SCANCODE_F7, "F8": sdl2.SDL_SCANCODE_F8, "F9": sdl2.SDL_SCANCODE_F9,
            "F10": sdl2.SDL_SCANCODE_F10, "F11": sdl2.SDL_SCANCODE_F11, "F12": sdl2.SDL_SCANCODE_F12,

            "LCTRL": sdl2.SDL_SCANCODE_LCTRL, "RCTRL": sdl2.SDL_SCANCODE_RCTRL,
            "LSHIFT": sdl2.SDL_SCANCODE_LSHIFT, "RSHIFT": sdl2.SDL_SCANCODE_RSHIFT,
            "LALT": sdl2.SDL_SCANCODE_LALT, "RALT": sdl2.SDL_SCANCODE_RALT,

            "TAB" : sdl2.SDL_SCANCODE_TAB, "CAPSLOCK" : sdl2.SDL_SCANCODE_CAPSLOCK,
            
            "HOME": sdl2.SDL_SCANCODE_HOME, "END": sdl2.SDL_SCANCODE_END,
            "INSERT": sdl2.SDL_SCANCODE_INSERT, "DELETE": sdl2.SDL_SCANCODE_DELETE,
            
            "RETURN": sdl2.SDL_SCANCODE_RETURN, "BACKSPACE": sdl2.SDL_SCANCODE_BACKSPACE,
            "SPACE": sdl2.SDL_SCANCODE_SPACE,
            
            "PLUS": sdl2.SDL_SCANCODE_KP_PLUS, "MINUS": sdl2.SDL_SCANCODE_KP_MINUS,
            "SLASH": sdl2.SDL_SCANCODE_SLASH, "BACKSLASH": sdl2.SDL_SCANCODE_BACKSLASH, 
            "ASTERISK": sdl2.SDL_SCANCODE_KP_MULTIPLY,
        }

        self.buttons = {
            "LEFT": sdl2.SDL_BUTTON_LEFT, "RIGHT": sdl2.SDL_BUTTON_RIGHT,
            "MIDDLE": sdl2.SDL_BUTTON_MIDDLE,
        }

    def event_handler(self, event):
        if event.type == sdl2.SDL_QUIT:
            self.destroy()

        self.input.update(event)

    def update_handler(self):
        if self.destroyed:
            self.engine.destroy()
            self.on_quit()

            if "on_quit" in self.functions:
                self.functions["on_quit"]()

        for layer in dict(sorted(self.engine.objects.items())):
            for object in self.engine.objects[layer]:
                if object.destroyed:
                    self.engine.objects[layer].pop(self.engine.objects[layer].index(object))

                else:
                    if object.enabled:
                        object.update()

                    for script in object.scripts:
                        if script.enabled:
                            script.update(self, object)

        sdl2.SDL_RenderClear(self.renderer)

        self.draw_handler()

        sdl2.SDL_SetRenderDrawColor(self.renderer, self.background_color.r, self.background_color.g, self.background_color.b, self.background_color.a)
        sdl2.SDL_RenderPresent(self.renderer)

        self.update()

        if "update" in self.functions:
            self.functions["update"]()

    def draw_handler(self):
        for layer in dict(sorted(self.engine.objects.items(), reverse = True)):
            for object in self.engine.objects[layer]:
                if object.destroyed:
                    self.engine.objects[layer].pop(self.engine.objects[layer].index(object))

                else:
                    if hasattr(object, "visible"):
                        if object.visible:
                            object.draw()

    def destroy(self):
        self.destroyed = True

        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    def bound(self, func):
        setattr(self.__class__, func.__name__, classmethod(func))

    def event(self, func):
        self.functions[func.__name__] = func

    def update(self):
        pass

    def on_quit(self):
        pass