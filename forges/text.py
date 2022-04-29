import sdl2, sdl2.sdlttf

import ctypes

from forges.color import Color
from forges.math import Vector2

import __main__

class Text:
    def __init__(self, text, font_file, font_size = 24, x = 0, y = 0, angle = 0, color = Color(6, 6, 8), parent = None, layer = 1):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.layer = layer

        if self.layer not in self.engine.objects[self.engine.current_window]:
            self.engine.objects[self.engine.current_window][self.layer] = []

        self.engine.objects[self.engine.current_window][self.layer].append(self)

        sdl2.sdlttf.TTF_Init()

        self.parent = parent

        if self.parent != None:
            self.set_parent(parent)

        self.offset = Vector2(0, 0)

        self.text = text

        self.font_file = font_file
        self.font_size = font_size

        self.x = x
        self.y = y

        self.angle = angle
        self.color = color

        self.destroyed = False
        self.visible = True
        self.enabled = True

        self.scripts = []
        self.childs = []

        self.rect = sdl2.SDL_Rect(int(self.x), int(self.y))

        self.render()

    def update(self):
        pass

    def render(self):
        self.font = sdl2.sdlttf.TTF_OpenFont(self.font_file.encode(), self.font_size)
        self.surface = sdl2.sdlttf.TTF_RenderText_Blended(self.font, self.text.encode(), sdl2.SDL_Color(int(self.color.r), int(self.color.g), int(self.color.b), int(self.color.a)))
        self.texture = sdl2.SDL_CreateTextureFromSurface(self.engine.current_window.renderer, self.surface)
        self.rendered_text = self.text
        self.rendered_font_size = self.font_size
        self.rendered_font_file = self.font_file

        self.rect.x, self.rect.y = int(self.x), int(self.y)

        w = ctypes.pointer(ctypes.c_int(0))
        h = ctypes.pointer(ctypes.c_int(0))

        sdl2.SDL_QueryTexture(self.texture, None, None, w, h)
        
        self.width, self.height = w.contents.value, h.contents.value
        self.rect.w, self.rect.h = self.width, self.height
   
    def draw(self):
        if not self.destroyed:
            if self.visible:
                if self.parent != None:
                    if hasattr(self.parent, "x") and hasattr(self.parent, "y"):
                        self.offset.x += self.parent.x
                        self.offset.y += self.parent.y

                    if hasattr(self.parent, "angle"):
                        self.angle = self.parent.angle

                self.x += self.offset.x
                self.y += self.offset.y

                if self.rendered_text != self.text or self.rendered_font_size != self.font_size or self.rendered_font_file != self.font_file:
                    self.render()
                    self.width = self.get_width()
                    self.height = self.get_height()

                if self.angle >= 360:
                    self.angle -= 360

                if self.angle <= -360:
                    self.angle += 360

                self.rect.x, self.rect.y = int(self.x), int(self.y)

                sdl2.SDL_RenderCopyEx(self.engine.current_window.renderer, self.texture, None, self.rect, self.angle, sdl2.SDL_Point(int(self.width / 2), int(self.height / 2)), sdl2.SDL_FLIP_NONE)

                self.x -= self.offset.x
                self.y -= self.offset.y

                if self.parent != None:
                    if hasattr(self.parent, "x") and hasattr(self.parent, "y"):
                        self.offset.x -= self.parent.x
                        self.offset.y -= self.parent.y

    def set_parent(self, parent):
        self.parent = parent
        self.parent.add_child(self)

    def get_parent(self):
        return self.parent

    def add_child(self, child):
        self.childs.append(child)

    def remove_child(self, child):
        self.childs.pop(self.childs.index(child))

    def get_childs(self):
        return self.childs

    def get_width(self):
        return self.width

    def get_height(self):
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

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_font_file(self, font_file):
        self.font_file = font_file
        self.render()

    def get_font_file(self):
        return self.font_file

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.render()
        self.width = self.get_width()
        self.height = self.get_height()

    def get_font_size(self):
        return self.font_size

    def set_text(self, text):
        self.text = text
        self.render()
        self.width = self.get_width()
        self.height = self.get_height()

    def get_text(self):
        return self.text

    def center(self):
        if not self.destroyed:
            self.x = self.engine.current_window.width / 2 - self.width / 2
            self.y = self.engine.current_window.height / 2 - self.height / 2

    def center_x(self):
        if not self.destroyed:
            self.x = self.engine.current_window.width / 2 - self.width / 2

    def center_y(self):
        if not self.destroyed:
            self.y = self.engine.current_window.height / 2 - self.height / 2

    def hit(self, entity):
        if not self.destroyed:
            for i in self.childs:
                if i.hit(entity):
                    return True

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

    def bound(self, func):
        setattr(self.__class__, func.__name__, classmethod(func))