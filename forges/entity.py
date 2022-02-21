import sdl2
import sdl2.ext

from forges.color import Color
from forges.math import Vector2

import __main__

class Entity:
    def __init__(self, width = 100, height = 100, x = 0, y = 0, color = Color(240, 240, 240), fill = True, parent = None, layer = 1):
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

        self.color = color
        self.fill = fill

        self.destroyed = False
        self.visible = True
        self.enabled = True

        self.scripts = []

        self.rect = sdl2.SDL_FRect(self.x, self.y, self.width, self.height)

    def update(self):
        pass

    def draw(self):
        if not self.destroyed:
            if self.visible:
                if self.parent != None:
                    self.x += self.parent.x
                    self.y += self.parent.y

                sdl2.SDL_SetRenderDrawColor(self.engine.window.renderer, self.color.r, self.color.g, self.color.b, self.color.a)

                self.rect = sdl2.SDL_FRect(self.x, self.y, self.width, self.height)

                sdl2.SDL_RenderDrawRectF(self.engine.window.renderer, self.rect)

                if self.fill:
                    sdl2.SDL_RenderFillRectF(self.engine.window.renderer, self.rect)

                self.rect = sdl2.SDL_FRect(self.x, self.y, self.width, self.height)

                if self.parent != None:
                    self.x -= self.parent.x
                    self.y -= self.parent.y

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
   
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

    def hit(self, entity):
        if not self.destroyed:
            if isinstance(entity, Vector2):
                left, top, right, bottom = self.rect.x, self.rect.y, self.rect.x + self.rect.w, self.rect.y + self.rect.h
                bleft, btop, bright, bbottom = entity.x, entity.y, entity.x, entity.y

            else:
                left, top, right, bottom = self.rect.x, self.rect.y, self.rect.x + self.rect.w, self.rect.y + self.rect.h
                bleft, btop, bright, bbottom = entity.rect.x, entity.rect.y, entity.rect.x + entity.rect.w, entity.rect.y + entity.rect.h
                
            return (bleft < right and bright > left and btop < bottom and bbottom > top)

        else:
            return False

    def hit2(self, entity, collision_tolreance = 10):
        if self.hit(entity):
            left, top, right, bottom = self.rect.x, self.rect.y, self.rect.x + self.rect.w, self.rect.y + self.rect.h
            bleft, btop, bright, bbottom = entity.rect.x, entity.rect.y, entity.rect.x + entity.rect.w, entity.rect.y + entity.rect.h

            if abs(btop - bottom) < collision_tolreance:
                return "bottom"

            elif abs(bbottom - top) < collision_tolreance:
                return "top"

            elif abs(bright - left) < collision_tolreance:
                return "left"

            elif abs(bleft - right) < collision_tolreance:
                return "right"

            else:
                return "unknown"
        
        else:
            return ""

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