import sdl2, sdl2.ext, sdl2.sdlmixer

import __main__

class Mixer:
    def __init__(self, file, volume = 1.0, layer = 1):
        if hasattr(__main__.forges, "forges"):
            self.engine = __main__.forges.forges

        else:
            self.engine = __main__.forges

        self.layer = layer

        if self.layer not in self.engine.objects:
            self.engine.objects[self.layer] = []

        self.engine.objects[self.layer].append(self)

        self.file = file
        self.volume = volume

        sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO)

        sdl2.sdlmixer.Mix_OpenAudio(44100, sdl2.sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)

        self.music = sdl2.sdlmixer.Mix_LoadMUS(self.file.encode())

        sdl2.sdlmixer.Mix_VolumeMusic(int(self.volume * 128))

        self.destroyed = False
        self.enabled = True

        self.scripts = []

    def update(self):
        pass

    def play(self, loop = 0):
        if not self.destroyed:
            sdl2.sdlmixer.Mix_PlayMusic(self.music, loop)

    def stop(self):
        sdl2.sdlmixer.Mix_HaltMusic()

    def pause(self):
        sdl2.sdlmixer.Mix_PauseMusic()

    def resume(self):
        if not self.destroyed:
            sdl2.sdlmixer.Mix_ResumeMusic()

    def set_volume(self, volume):
        self.volume = volume
        sdl2.sdlmixer.Mix_VolumeMusic(int(self.volume * 128))

    def get_volume(self):
        return self.volume

    def set_pos(self, pos):
        sdl2.sdlmixer.Mix_SetMusicPosition(pos)

    def fade_in(self, duration = 1000, loop = 0):
        if not self.destroyed:
            sdl2.sdlmixer.Mix_FadeInMusic(self.music, loop, duration)

    def fade_out(self, duration = 1000):
        sdl2.sdlmixer.Mix_FadeOutMusic(duration)

    def destroy(self):
        self.stop()
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