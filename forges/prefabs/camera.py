import forges, random, time

class Camera(forges.Object):
    def __init__(self):
        super().__init__()

        self.x = 0
        self.y = 0

        self.static_objects = []
        self.shakes = []
        self.last_shake = 0

    def update(self):
        for log in self.shakes:
            if log[0]: self.x -= log[1]
            else: self.y -= log[1]

        self.shakes.clear()

        for layer in dict(sorted(self.engine.objects.items(), reverse = True)):
            if layer > 0:
                for object in self.engine.objects[layer]:
                    if object not in self.static_objects:
                        if hasattr(object, "offset"):
                            object.offset.x = -self.x
                            object.offset.y = -self.y
                
    def shake(self, force = 10, shake_wait = 0.01):
        if self.last_shake + shake_wait < time.time():
            self.last_shake = time.time()
            x, y = random.randint(-force, force), random.randint(-force, force)
            self.shakes += [(x, True), (y, False)]
            self.x += x
            self.y += y

    def add_static_object(self, object):
        self.static_objects.append(object)
        self.static_objects += object.childs

    def set_pos_smooth(self, vec2, value):
        self.x, self.y = forges.math.lerp(self.x, vec2.x, value), forges.math.lerp(self.y, vec2.y, value)

    def set_pos(self, vec2):
        self.x, self.y = vec2.x, vec2.y

    def get_pos(self):
        return forges.math.Vector2(self.x, self.y)

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y