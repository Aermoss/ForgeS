from forges.entity import Entity
from forges.sprite import Sprite
from forges.color import Color
from forges.math import lerp

import time

class Intro(Entity):
    def __init__(self):
        super().__init__(color = Color(0, 0, 0, 255), layer = -1)

        self.logo = Sprite(self.engine.path + "/assets/logo/logo.png", alpha = 0, width = 350, height = 80, layer = -1)
        self.logo.update = self.update_logo

        self.target_alpha = self.color.a
        self.target_logo_alpha = self.logo.alpha

    def update_logo(self):
        self.logo.center()

        if self.engine.current_window.start_time + 5 < time.time():
            self.target_logo_alpha = lerp(self.target_logo_alpha, 0, 0.05)
            self.logo.set_alpha(int(self.target_logo_alpha))

            if self.logo.alpha == 0:
                self.logo.destroy()

        elif self.engine.current_window.start_time + 0.5 < time.time():
            self.target_logo_alpha = lerp(self.target_logo_alpha, 255, 0.01)
            self.logo.set_alpha(int(self.target_logo_alpha))

    def update(self):
        self.width = self.engine.current_window.width
        self.height = self.engine.current_window.height

        if self.engine.current_window.start_time + 7 < time.time():
            self.target_alpha = lerp(self.target_alpha, 0, 0.1)
            self.color.a = int(self.target_alpha)

            if self.color.a == 0:
                self.destroy()