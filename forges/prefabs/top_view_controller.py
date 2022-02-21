import forges

class TopViewController(forges.Entity):
    def __init__(self, width = 50, height = 100, x = 0, y = 0, color = forges.color.Color(20, 20, 20), fill = True, layer = 1, speed = 3, sprint_speed = 6):
        super().__init__(width = width, height = height, x = x, y = y, color = color, fill = fill, layer = layer)

        self.window = forges.forges.get_window()

        self.speed = speed
        self.sprint_speed = sprint_speed

        self.target_speed = speed

    def update(self):
        if self.window.input.key_pressed(self.window.keys["LSHIFT"]):
            self.target_speed = self.sprint_speed

        else:
            self.target_speed = self.speed

        if self.window.input.key_pressed(self.window.keys["S"]):
            self.y += self.target_speed

        if self.window.input.key_pressed(self.window.keys["W"]):
            self.y -= self.target_speed

        if self.window.input.key_pressed(self.window.keys["D"]):
            self.x += self.target_speed

        if self.window.input.key_pressed(self.window.keys["A"]):
            self.x -= self.target_speed