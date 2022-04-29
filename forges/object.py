import sdl2, sdl2.ext

import __main__

class Object:
    def __init__(self, parent = None, layer = 1):
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

        self.destroyed = False
        self.enabled = True

        self.scripts = []
        self.childs = []

    def update(self):
        pass

    def destroy(self):
        for i in self.childs:
            i.destroy()

        self.destroyed = True
        self.engine.objects[self.engine.current_window][self.layer].pop(self.engine.objects[self.engine.current_window][self.layer].index(self))

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