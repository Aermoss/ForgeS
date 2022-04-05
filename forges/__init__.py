import forges.color as color
import forges.math as math

from forges.font_manager import FontManager
from forges.error import ForgeError
from forges.build import Builder
from forges.main import ForgeS
from forges.window import Window
from forges.input import Input
from forges.script import Script
from forges.object import Object
from forges.entity import Entity
from forges.sprite import Sprite
from forges.text import Text
from forges.mixer import Mixer
from forges.animation import Animation
from forges.intro import Intro

import forges.prefabs as prefabs
import forges.scripts as scripts

forges = ForgeS()
fonts = FontManager(forges).get()

def run():
    forges.run()

def get():
    return forges

def import_sdl2():
    global sdl2
    import sdl2