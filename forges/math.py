from forges.color import Color
from forges.error import ForgeError

def lerp(a, b, value):
    if isinstance(a, int) or isinstance(a, float):
        return a + (b - a) * value

    if isinstance(a, tuple):
        if len(a) != len(b):
            raise ForgeError("Tuple sizes doesn't match")

        new = []

        for i in a:
            new.append(lerp(i, b[a.index(i)], value))

        return tuple(new)

    elif isinstance(a, Vector2):
        return Vector2(lerp(a.x, b.x, value), lerp(a.y, b.y, value))

    elif isinstance(a, Vector3):
        return Vector3(lerp(a.x, b.x, value), lerp(a.y, b.y, value), lerp(a.z, b.z, value))

    elif isinstance(a, Color):
        return Color(lerp(a.r, b.r, value), lerp(a.g, b.g, value), lerp(a.b, b.b, value), lerp(a.a, b.a, value))

class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def get(self):
        return (self.x, self.y)

    def copy(self):
        return Vector2(self.x, self.y)

    def __add__(self, value):
        return Vector2(self.x + value.x, self.y + value.y)

    def __sub__(self, value):
        return Vector2(self.x - value.x, self.y - value.y)

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector2(self.x * value, self.y * value)

        return Vector2(self.x * value.x, self.y * value.y)

    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            return Vector2(self.x / value, self.y / value)

        return Vector2(self.x / value.x, self.y / value.y)
    
    def __repr__(self):
        return "Vector2" + str((self.x, self.y))

class Vector3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def get(self):
        return (self.x, self.y, self.z)

    def copy(self):
        return Vector3(self.x, self.y, self.z)

    def __add__(self, value):
        return Vector3(self.x + value.x, self.y + value.y, self.z + value.z)

    def __sub__(self, value):
        return Vector3(self.x - value.x, self.y - value.y, self.z - value.z)

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector3(self.x * value, self.y * value, self.z * value)

        return Vector3(self.x * value.x, self.y * value.y, self.z * value.z)

    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            return Vector3(self.x / value, self.y / value, self.z / value)

        return Vector3(self.x / value.x, self.y / value.y, self.z / value.z)
    
    def __repr__(self):
        return "Vector3" + str((self.x, self.y, self.z))