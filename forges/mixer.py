import sdl2, sdl2.ext, sdl2.sdlmixer

import __main__

class Mixer:
    def __init__(self, file, volume = 255, parent = None, layer = 1):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.layer = layer

        if self.layer not in self.engine.objects[self.engine.current_window]:
            self.engine.objects[self.engine.current_window][self.layer] = []

        self.engine.objects[self.engine.current_window][self.layer].append(self)

        self.file = file
        self.volume = volume
        self.parent = parent

        if self.parent != None:
            self.set_parent(parent)

        sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO)

        sdl2.sdlmixer.Mix_OpenAudio(44100, sdl2.sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)

        self.music = sdl2.sdlmixer.Mix_LoadWAV(self.file.encode())

        self.destroyed = False
        self.enabled = True

        self.scripts = []
        self.childs = []

    def update(self):
        pass

    def play(self, loop = 0):
        if not self.destroyed:
            self.channel = sdl2.sdlmixer.Mix_PlayChannel(-1, self.music, loop)
            sdl2.sdlmixer.Mix_Volume(self.channel, int(self.volume / 2))

    def stop(self):
        sdl2.sdlmixer.Mix_HaltChannel(self.channel)

    def pause(self):
        sdl2.sdlmixer.Mix_Pause(self.channel)

    def resume(self):
        if not self.destroyed:
            sdl2.sdlmixer.Mix_Resume(self.channel)

    def set_volume(self, volume):
        self.volume = volume
        sdl2.sdlmixer.Mix_Volume(self.channel, int(self.volume / 2))

    def get_volume(self):
        return self.volume

    def fade_in(self, duration = 1000, loop = 0):
        if not self.destroyed:
            self.channel = sdl2.sdlmixer.Mix_FadeInChannel(-1, self.music, loop, duration)
            sdl2.sdlmixer.Mix_Volume(self.channel, int(self.volume / 2))

    def fade_out(self, duration = 1000):
        sdl2.sdlmixer.Mix_FadeOutChannel(self.channel, duration)

    def set_file(self, file):
        self.file = file
        self.music = sdl2.sdlmixer.Mix_LoadMUS(self.file.encode())

    def get_file(self):
        return self.file

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

    def destroy(self):
        for i in self.childs:
            i.destroy()
            
        self.stop()
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