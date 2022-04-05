import forges

from forges.prefabs.button import Button

class CheckBox(Button):
    def __init__(self, normal_color = forges.color.Color(200, 200, 200), press_color = forges.color.Color(100, 100, 100), highlight_color = forges.color.Color(150, 150, 150), width = 20, height = 20, x = 0, y = 0, color = forges.color.Color(6, 6, 8), fill = True, parent = None, layer = 1):
        super().__init__(normal_color = normal_color, press_color = press_color, highlight_color = highlight_color, width = width, height = height, x = x, y = y, color = color, fill = fill, parent = parent, layer = layer)

        self.functions["on_release"] = self.update_state
        self.state = False

        self.box = forges.Entity(width = self.width - 10, height = self.height - 10, x = 5, y = 5, parent = self)
        self.box.visible = False

    def update_state(self):
        self.state = not self.state
        self.box.visible = True if self.state else False

    def get_state(self):
        return self.state