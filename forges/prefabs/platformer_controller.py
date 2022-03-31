import forges

class PlatformerController(forges.Entity):
    def __init__(self, speed = 5, sprint_speed = 10, jumpforce = -13, width = 50, height = 100, x = 0, y = 0, color = forges.color.Color(6, 6, 8), fill = True, parent = None, layer = 1):
        super().__init__(width = width, height = height, x = x, y = y, color = color, fill = fill, parent = parent, layer = layer)

        self.window = forges.forges.get_window()

        self.speed = speed
        self.sprint_speed = sprint_speed
        self.jumpforce = jumpforce

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