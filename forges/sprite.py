import sdl2
import sdl2.ext

import ctypes

from forges.math import Vector2

import __main__

class Sprite:
    def __init__(self, file, width = 100, height = 100, x = 0, y = 0, alpha = 255, parent = None, layer = 1):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.layer = layer

        if self.layer not in self.engine.objects:
            self.engine.objects[self.layer] = []

        self.engine.objects[self.layer].append(self)

        self.parent = parent

        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.alpha = alpha

        self.file = file

        self.scripts = []

        self.destroyed = False
        self.visible = True
        self.enabled = True

        self.image = sdl2.sdlimage.IMG_LoadTexture(self.engine.window.renderer, self.file.encode())
        sdl2.SDL_SetTextureAlphaMod(self.image, alpha)
        sdl2.SDL_QueryTexture(self.image, None, None, ctypes.c_int(self.width), ctypes.c_int(self.height))
        self.rect = sdl2.SDL_FRect(self.x, self.y, self.width * 2, self.height * 2)

    def update(self):
        pass

    def draw(self):
        if not self.destroyed:
            if self.visible:
                if self.parent != None:
                    self.x += self.parent.x
                    self.y += self.parent.y

                self.rect = sdl2.SDL_FRect(self.x, self.y, self.width, self.height)
                
                sdl2.SDL_RenderCopyF(self.engine.window.renderer, self.image, None, self.rect)

                self.rect = sdl2.SDL_FRect(self.x, self.y, self.width, self.height)

                if self.parent != None:
                    self.x -= self.parent.x
                    self.y -= self.parent.y

    def load_image(self, file):
        self.file = file
        self.image = sdl2.sdlimage.IMG_LoadTexture(self.engine.window.renderer, self.file.encode())
        sdl2.SDL_SetTextureAlphaMod(self.image, self.alpha)
        sdl2.SDL_QueryTexture(self.image, None, None, ctypes.c_int(self.width), ctypes.c_int(self.height))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        if alpha > 0:
            self.alpha = alpha

        else:
            self.alpha = 0
            
        sdl2.SDL_SetTextureAlphaMod(self.image, int(self.alpha))

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

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

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def hit(self, entity):
        if not self.destroyed:
            if isinstance(entity, Vector2):
                left, top, right, bottom = self.rect.x, self.rect.y, self.rect.x + self.rect.w, self.rect.y + self.rect.h
                bleft, btop, bright, bbottom = entity.x, entity.y, entity.x, entity.y

            elif isinstance(entity, tuple):
                left, top, right, bottom = self.rect.x, self.rect.y, self.rect.x + self.rect.w, self.rect.y + self.rect.h
                bleft, btop, bright, bbottom = entity[0], entity[1], entity[0], entity[1]

            else:
                left, top, right, bottom = self.rect.x, self.rect.y, self.rect.x + self.rect.w, self.rect.y + self.rect.h
                bleft, btop, bright, bbottom = entity.rect.x, entity.rect.y, entity.rect.x + entity.rect.w, entity.rect.y + entity.rect.h
                
            return (bleft < right and bright > left and btop < bottom and bbottom > top)

        else:
            return False
    
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

    def play_animation(self, animation):
        animation.pos = animation.pos + animation.time

        if animation.pos >= len(animation.frames):
            animation.pos = 0

        self.load_image(f"{animation.folder}/{animation.frames[int(animation.pos)]}")

        self.draw()