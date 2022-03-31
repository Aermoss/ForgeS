import forges

class TopViewController(forges.Entity):
    def __init__(self, speed = 5, sprint_speed = 10, width = 50, height = 100, x = 0, y = 0, color = forges.color.Color(6, 6, 8), fill = True, parent = None, layer = 1):
        super().__init__(width = width, height = height, x = x, y = y, color = color, fill = fill, parent = parent, layer = layer)

        self.window = forges.forges.get_window()

        self.speed = 3
        self.sprint_speed = 6

        self.target_speed = self.speed

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