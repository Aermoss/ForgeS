import sdl2, sdl2.ext

from forges.color import Color
from forges.math import Vector2

import __main__

class Entity:
    def __init__(self, width = 100, height = 100, x = 0, y = 0, color = Color(6, 6, 8), fill = True, parent = None, layer = 1):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.layer = layer

        if self.layer not in self.engine.objects[self.engine.current_window]:
            self.engine.objects[self.engine.current_window][self.layer] = []

        self.engine.objects[self.engine.current_window][self.layer].append(self)

        self.parent = parent

        if self.parent != None:
            self.set_parent(parent)

        self.offset = Vector2(0, 0)

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
        self.childs = []

        self.rect = sdl2.SDL_Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def update(self):
        pass

    def draw(self):
        if not self.destroyed:
            if self.visible:
                if self.parent != None:
                    if hasattr(self.parent, "x") and hasattr(self.parent, "y"):
                        self.offset.x += self.parent.x
                        self.offset.y += self.parent.y

                self.x += self.offset.x
                self.y += self.offset.y

                self.rect.x, self.rect.y, self.rect.w, self.rect.h = int(self.x), int(self.y), int(self.width), int(self.height)

                sdl2.SDL_SetRenderDrawColor(self.engine.current_window.renderer, int(self.color.r), int(self.color.g), int(self.color.b), int(self.color.a))

                if self.fill:
                    sdl2.SDL_RenderFillRect(self.engine.current_window.renderer, self.rect)

                else:
                    sdl2.SDL_RenderDrawRect(self.engine.current_window.renderer, self.rect)

                self.x -= self.offset.x
                self.y -= self.offset.y

                if self.parent != None:
                    if hasattr(self.parent, "x") and hasattr(self.parent, "y"):
                        self.offset.x -= self.parent.x
                        self.offset.y -= self.parent.y

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

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
        for i in self.childs:
            i.destroy()

        self.destroyed = True
        self.engine.objects[self.engine.current_window][self.layer].pop(self.engine.objects[self.engine.current_window][self.layer].index(self))

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