import forges

class PlatformerController(forges.Entity):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.window = forges.forges.get_window()

        self.speed = 5
        self.sprint_speed = 10
        self.jumpforce = -13

        for i in kwargs:
            setattr(self, i, kwargs[i])

        self.target_speed = self.speed
        self.add_script(forges.scripts.Gravity())
    
    def add_object(self, object):
        self.get_script(0).add_object(object)

    def update(self):
        if self.window.input.key_pressed(self.window.keys["LSHIFT"]):
            self.target_speed = self.sprint_speed

        else:
            self.target_speed = self.speed

        if self.window.input.key_pressed(self.window.keys["D"]):
            self.x += self.target_speed

        if self.window.input.key_pressed(self.window.keys["A"]):
            self.x -= self.target_speed

        if self.window.input.key_pressed(self.window.keys["SPACE"]):
            if self.get_script(0).grounded:
                self.get_script(0).grounded = False
                self.get_script(0).force(forges.math.Vector2(0, self.jumpforce))