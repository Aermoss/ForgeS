import sdl2, sdl2.sdlttf

import ctypes

from forges.color import Color
from forges.math import Vector2

import __main__

class Text:
    def __init__(self, text, font_file, font_size = 24, x = 0, y = 0, color = Color(20, 20, 20), parent = None, layer = 1):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.layer = layer

        if self.layer not in self.engine.objects:
            self.engine.objects[self.layer] = []

        self.engine.objects[self.layer].append(self)

        self.parent = parent

        self.text = text

        self.font_file = font_file
        self.font_size = font_size

        self.x = x
        self.y = y

        self.color = color

        sdl2.sdlttf.TTF_Init()

        self.font = sdl2.sdlttf.TTF_OpenFont(self.font_file.encode(), self.font_size)
        self.surface = sdl2.sdlttf.TTF_RenderText_Blended(self.font, self.text.encode(), sdl2.SDL_Color(self.color.r, self.color.g, self.color.b, self.color.a))
        self.texture = sdl2.SDL_CreateTextureFromSurface(self.engine.window.renderer, self.surface)

        self.width = self.get_width()
        self.height = self.get_height()

        self.destroyed = False
        self.visible = True
        self.enabled = True

        self.scripts = []

    def update(self):
        pass
   
    def draw(self):
        if not self.destroyed:
            if self.visible:
                if self.parent != None:
                    self.x += self.parent.x
                    self.y += self.parent.y

                dst = sdl2.SDL_FRect(self.x, self.y)

                w = ctypes.pointer(ctypes.c_int(0))
                h = ctypes.pointer(ctypes.c_int(0))

                sdl2.SDL_QueryTexture(self.texture, None, None, w, h)

                self.width, self.height = w.contents.value, h.contents.value
                dst.w, dst.h = self.width, self.height

                sdl2.SDL_RenderCopyF(self.engine.window.renderer, self.texture, None, dst)

                if self.parent != None:
                    self.x -= self.parent.x
                    self.y -= self.parent.y

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_width(self):
        dst = sdl2.SDL_FRect(self.x, self.y)

        w = ctypes.pointer(ctypes.c_int(0))
        h = ctypes.pointer(ctypes.c_int(0))

        sdl2.SDL_QueryTexture(self.texture, None, None, w, h)

        self.width, self.height = w.contents.value, h.contents.value
        dst.w, dst.h = self.width, self.height

        return self.width

    def get_height(self):
        dst = sdl2.SDL_FRect(self.x, self.y)

        w = ctypes.pointer(ctypes.c_int(0))
        h = ctypes.pointer(ctypes.c_int(0))

        sdl2.SDL_QueryTexture(self.texture, None, None, w, h)
        
        self.width, self.height = w.contents.value, h.contents.value
        dst.w, dst.h = self.width, self.height

        return self.height

    def set_pos(self, vector2):
        self.x, self.y = vector2.x, vector2.y

    def get_pos(self):
        return Vector2(self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_font_file(self, font_file):
        self.font_file = font_file
        self.font = sdl2.sdlttf.TTF_OpenFont(self.font_file.encode(), self.font_size)
        self.surface = sdl2.sdlttf.TTF_RenderText_Blended(self.font, self.text.encode(), sdl2.SDL_Color(self.color.r, self.color.g, self.color.b, self.color.a))
        self.texture = sdl2.SDL_CreateTextureFromSurface(self.engine.window.renderer, self.surface)

    def get_font_file(self):
        return self.font_file

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.font = sdl2.sdlttf.TTF_OpenFont(self.font_file.encode(), self.font_size)
        self.surface = sdl2.sdlttf.TTF_RenderText_Blended(self.font, self.text.encode(), sdl2.SDL_Color(self.color.r, self.color.g, self.color.b, self.color.a))
        self.texture = sdl2.SDL_CreateTextureFromSurface(self.engine.window.renderer, self.surface)
        self.width = self.get_width()
        self.height = self.get_height()

    def get_font_size(self):
        return self.font_size

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def center(self):
        if not self.destroyed:
            self.x = self.engine.window.width / 2 - self.width / 2
            self.y = self.engine.window.height / 2 - self.height / 2

    def center_x(self):
        if not self.destroyed:
            self.x = self.engine.window.width / 2 - self.width / 2

    def center_y(self):
        if not self.destroyed:
            self.y = self.engine.window.height / 2 - self.height / 2

    def destroy(self):
        self.destroyed = True
        self.engine.objects[self.layer].pop(self.engine.objects[self.layer].index(self))

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

    def bound(self, func):
        setattr(self.__class__, func.__name__, classmethod(func))