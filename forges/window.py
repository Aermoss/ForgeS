import sdl2, sdl2.ext

import os, ctypes, time

from forges.input import Input
from forges.color import Color
from forges.intro import Intro

import __main__

class Window:
    def __init__(self, width = 1200, height = 600, vsync = True, fullscreen = False, always_on_top = False, opengl = False, resizable = False, background_color = Color(255, 255, 255, 255), intro = True):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.engine.add_window(self)

        self.user32 = ctypes.windll.user32
        self.monitor_width,self.monitor_height = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)

        self.width = width
        self.height = height
        self.vsync = vsync
        self.fullscreen = fullscreen
        self.background_color = background_color
        self.always_on_top = always_on_top
        self.opengl = opengl
        self.resizable = resizable

        self.start_time = time.time()
        self.destroyed = False
        self.enabled = True
        self.functions = {}
        self.scripts = []

        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        window_flags = sdl2.SDL_WINDOW_SHOWN
        if self.fullscreen: window_flags |= sdl2.SDL_WINDOW_FULLSCREEN
        if self.always_on_top: window_flags |= sdl2.SDL_WINDOW_ALWAYS_ON_TOP
        if self.opengl: window_flags |= sdl2.SDL_WINDOW_OPENGL
        if self.resizable: window_flags |= sdl2.SDL_WINDOW_RESIZABLE

        self.window = sdl2.SDL_CreateWindow("Forge S".encode(), sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, self.width, self.height, window_flags)
        
        if self.opengl: self.context = sdl2.SDL_GL_CreateContext(self.window)
        else:
            renderer_flags = 0
            if self.vsync: renderer_flags = sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC

            self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, renderer_flags)

            sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_BLEND)

        self.path = self.engine.path

        icon = self.path + "\\assets\\icon\\icon.png"
        icon = sdl2.ext.load_image(icon)
        sdl2.SDL_SetWindowIcon(self.window, icon)

        self.input = Input(self)

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

        if intro and not self.opengl:
            self.intro = Intro()

        else:
            self.intro = None

    def event_handler(self, event):
        if event.type == sdl2.SDL_WINDOWEVENT and event.window.event == sdl2.SDL_WINDOWEVENT_CLOSE:
            if event.window.windowID == sdl2.SDL_GetWindowID(self.window):
                self.destroy()

        self.input.update(event)

    def update_handler(self):
        if self.destroyed:
            self.destroy()
            self.on_quit()

            if "on_quit" in self.functions:
                self.functions["on_quit"]()

            return

        for script in self.scripts:
            if script.enabled:
                script.update(self, self)

        for layer in dict(sorted(self.engine.objects[self.engine.current_window].items())):
            for object in self.engine.objects[self.engine.current_window][layer]:
                if object.destroyed:
                    self.engine.objects[self.engine.current_window][layer].pop(self.engine.objects[self.engine.current_window][layer].index(object))

                else:
                    if object.enabled:
                        object.update()

                    for script in object.scripts:
                        if script.enabled:
                            script.update(self, object)

        self.draw_handler()

        if self.enabled:
            self.update()

        if "update" in self.functions:
            self.functions["update"]()

    def draw_handler(self):
        if "on_draw" in self.functions:
            self.functions["on_draw"]()

        if self.opengl:
            sdl2.SDL_GL_SwapWindow(self.window)
            return

        sdl2.SDL_SetRenderDrawColor(self.renderer, self.background_color.r, self.background_color.g, self.background_color.b, self.background_color.a)
        sdl2.SDL_RenderClear(self.renderer)

        for layer in dict(sorted(self.engine.objects[self.engine.current_window].items(), reverse = True)):
            for object in self.engine.objects[self.engine.current_window][layer]:
                if object.destroyed:
                    self.engine.objects[self.engine.current_window][layer].pop(self.engine.objects[self.engine.current_window][layer].index(object))

                else:
                    if hasattr(object, "visible"):
                        if object.visible:
                            if hasattr(object, "on_draw"):
                                object.on_draw()

                            object.draw()

        sdl2.SDL_RenderPresent(self.renderer)

    def set_fullscreen(self, fullscreen = True):
        self.fullscreen = fullscreen

        if self.fullscreen:
            sdl2.SDL_SetWindowFullscreen(self.window, sdl2.SDL_WINDOW_FULLSCREEN)

            if "on_fullscreen_change" in self.functions:
                self.functions["on_fullscreen_change"](True)

        else:
            sdl2.SDL_SetWindowFullscreen(self.window, 0)

            if "on_fullscreen_change" in self.functions:
                self.functions["on_fullscreen_change"](False)

    def intro_finished(self):
        if self.intro == None: return None
        return True if self.intro.destroyed else False

    def set_width(self, width):
        self.width = width
        sdl2.SDL_SetWindowSize(self.window, self.width, self.height)

    def set_height(self, height):
        self.height = height
        sdl2.SDL_SetWindowSize(self.window, self.width, self.height)

    def set_size(self, width, height):
        self.width, self.height = width, height
        sdl2.SDL_SetWindowSize(self.window, self.width, self.height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return self.width, self.height

    def get_monitor_width(self):
        self.monitor_width = self.user32.GetSystemMetrics(0)
        return self.monitor_width

    def get_monitor_height(self):
        self.monitor_height = self.user32.GetSystemMetrics(1)
        return self.monitor_height

    def get_monitor_size(self):
        self.monitor_width,self.monitor_height = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)
        return self.monitor_width,self.monitor_height

    def set_always_on_top(self, always_on_top = True):
        self.always_on_top = always_on_top
        sdl2.SDL_SetWindowAlwaysOnTop(self.window, self.always_on_top)

    def destroy(self):
        self.destroyed = True
        self.enabled = False

        self.engine.windows.pop(self.engine.windows.index(self))
        del self.engine.objects[self]
        if self.engine.current_window == self: self.engine.current_window = None

        if not self.opengl: sdl2.SDL_DestroyRenderer(self.renderer)
        else: sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.window)

    def bound(self, func):
        setattr(self.__class__, func.__name__, classmethod(func))

    def event(self, func):
        self.functions[func.__name__] = func

    def add_script(self, script):
        self.scripts.append(script)

    def get_script(self, index):
        return self.scripts[index]

    def remove_script(self, script):
        self.scripts.pop(self.scripts.index(script))

    def enable(self, scripts = True):
        if scripts:
            for script in self.scripts:
                script.enable()

        self.enabled = True

    def disable(self, scripts = True):
        if scripts:
            for script in self.scripts:
                script.disable()

        self.enabled = False

    def update(self):
        pass

    def on_quit(self):
        pass