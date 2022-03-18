import forges

class Gravity(forges.Script):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.acceleration = forges.math.Vector2(0, 0.5)
        self.velocity = forges.math.Vector2(0, 0)
        self.friction = -0.01

        self.objects = []

        for i in kwargs:
            setattr(self, i, kwargs[i])

    def add_object(self, object):
        self.objects.append(object)

    def force(self, force):
        self.velocity += force

    def update(self, window, entity):
        self.acceleration = forges.math.Vector2(0, 0.5)
        self.grounded = False

        for i in self.objects:
            if i.hit(entity):
                if entity.y < i.y:
                    entity.y = i.y - entity.height
                    self.velocity = forges.math.Vector2(0, 0)
                    self.grounded = True

        if not self.grounded:
            self.acceleration.x += self.velocity.x * self.friction
            self.velocity += self.acceleration
            entity.set_pos(entity.get_pos() + self.velocity + forges.math.Vector2(0, 0.5) + self.acceleration)