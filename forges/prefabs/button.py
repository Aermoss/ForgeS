import forges

class Button(forges.Entity):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.width, self.height = 100, 40
        self.normal_color, self.press_color, self.highlight_color = forges.color.Color(200, 200, 200), forges.color.Color(100, 100, 100), forges.color.Color(150, 150, 150)

        self.color = forges.color.Color(self.normal_color.r, self.normal_color.g, self.normal_color.b, self.normal_color.a)

        for i in kwargs:
            setattr(self, i, kwargs[i])

        self.window = forges.get().get_window()
        self.functions = {}
        self.target_color = forges.color.Color(self.color.r, self.color.g, self.color.b, self.color.a)
        
    def update(self):
        if self.hit(self.window.input.mouse_pos()):
            if self.window.input.mouse_pressed(self.window.buttons["LEFT"]):
                self.press()

            else:
                if self.pressed:
                    self.release()

                self.highlight()

        else:
            self.natural()
            self.pressed = False

        self.color.r, self.color.g, self.color.b, self.color.a = int(self.target_color.r), int(self.target_color.g), int(self.target_color.b), int(self.target_color.a)

    def natural(self):
        self.target_color = forges.math.lerp(self.target_color, self.normal_color, 0.1)

    def press(self):
        self.pressed = True

        self.target_color = forges.math.lerp(self.target_color, self.press_color, 0.3)

        if "on_press" in self.functions:
            self.functions["on_press"]()

    def release(self):
        self.pressed = False

        self.target_color = forges.math.lerp(self.target_color, self.highlight_color, 0.1)

        if "on_release" in self.functions:
            self.functions["on_release"]()

    def highlight(self):
        self.pressed = False

        self.target_color = forges.math.lerp(self.target_color, self.highlight_color, 0.2)

        if "on_highlight" in self.functions:
            self.functions["on_highlight"]()

    def event(self, func):
        self.functions[func.__name__] = func