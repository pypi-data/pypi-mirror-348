import math


class Vector2:
    def __init__(self, x=None, y=None):
        self.x = 0
        self.y = 0

        if x is None:
            if y is None:
                self.x = 0
                self.y = 0
            else:
                self.x = y
                self.y = y
        else:
            if y is None:
                self.x = x
                self.y = x
            else:
                self.x = x
                self.y = y

        if x is list or x is tuple or x is set:
            self.x = x[0]
            self.y = x[1]

        if x is Vector2 or x is Vector3:
            self.x = x.x
            self.y = x.y

    def unwrap(self, to_tuple=False):
        return [self.x, self.y] if not to_tuple else (self.x, self.y)

    def normalized(self):
        return self / len(self)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def lerped_to(self, v2, t):
        return Vector2(v2) * t + self * (1 - t)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __sub__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)
        elif type(other) == int or type(other) == float:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        elif type(other) == int or type(other) == float:
            return Vector2(self.x * other, self.y * other)

    def __add__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) == int or type(other) == float:
            return Vector2(self.x + other, self.y + other)

    def __truediv__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x / other.x, self.y / other.y)
        elif type(other) == int or type(other) == float:
            return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x // other.x, self.y // other.y)
        elif type(other) == int or type(other) == float:
            return Vector2(self.x // other, self.y // other)

    def __mod__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x % other.x, self.y % other.y)
        elif type(other) == int or type(other) == float:
            return Vector2(self.x % other, self.y % other)

    def __pow__(self, power, modulo=None):
        if type(power) == Vector2:
            return Vector2(self.x ** power.x, self.y ** power.y)
        elif type(power) == int or type(power) == float:
            return Vector2(self.x ** power, self.y ** power)


class Vector3:
    def __init__(self, x=None, y=None, z=None):
        self.x = 0
        self.y = 0
        self.z = 0

        if x is None:
            if y is None:
                if z is None:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                else:
                    self.x = z
                    self.y = z
                    self.z = z
            else:
                if z is None:
                    self.x = y
                    self.y = y
                    self.z = y
                else:
                    self.x = 0
                    self.y = y
                    self.z = z
        else:
            if y is None:
                if z is None:
                    self.x = x
                    self.y = x
                    self.z = x
                else:
                    self.x = x
                    self.y = 0
                    self.z = z
            else:
                if z is None:
                    self.x = x
                    self.y = y
                    self.z = 0
                else:
                    self.x = x
                    self.y = y
                    self.z = z

        if x is list or x is tuple or x is set:
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]

        if x is Vector2:
            self.x = x.x
            self.y = x.y

        if x is Vector3:
            self.x = x.x
            self.y = x.y
            self.z = x.z

    def unwrap(self):
        return [self.x, self.y, self.z]

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        if other is Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif other is Vector2:
            return Vector3(self.x + other.x, self.y + other.y, self.z)
        elif other is int or other is float:
            return Vector3(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if other is Vector3:
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif other is Vector2:
            return Vector3(self.x - other.x, self.y - other.y, self.z)
        elif other is int or other is float:
            return Vector3(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if other is Vector3:
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif other is Vector2:
            return Vector3(self.x * other.x, self.y * other.y, self.z)
        elif other is int or other is float:
            return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if other is Vector3:
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif other is Vector2:
            return Vector3(self.x / other.x, self.y / other.y, self.z)
        elif other is int or other is float:
            return Vector3(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other):
        if other is Vector3:
            return Vector3(self.x // other.x, self.y // other.y, self.z // other.z)
        elif other is Vector2:
            return Vector3(self.x // other.x, self.y // other.y, self.z)
        elif other is int or other is float:
            return Vector3(self.x // other, self.y // other, self.z // other)

    def __mod__(self, other):
        if other is Vector3:
            return Vector3(self.x % other.x, self.y % other.y, self.z % other.z)
        elif other is Vector2:
            return Vector3(self.x % other.x, self.y % other.y, self.z)
        elif other is int or other is float:
            return Vector3(self.x % other, self.y % other, self.z % other)

    def __pow__(self, power, modulo=None):
        if power is Vector3:
            return Vector3(self.x ** power.x, self.y ** power.y, self.z ** power.z)
        elif power is Vector2:
            return Vector3(self.x ** power.x, self.y ** power.y, self.z)
        elif power is int or power is float:
            return Vector3(self.x ** power, self.y ** power, self.z ** power)


class Particle:
    t_circle = 0
    t_square = 1

    def __init__(self, type_, pos, speed, accel, size, size_decrease, color):
        self.pos = pos
        self.size = size
        self.type = type_
        self.speed = Vector2(speed)
        self.accel = Vector2(accel)
        self.size_decrease = size_decrease
        self.color = color

    def tick(self):
        self.size -= self.size_decrease
        self.speed += self.accel
        self.pos += self.speed

    def pack_for_draw(self, dis, out_library="pygame"):
        if out_library.lower() == "pygame":
            if self.type == self.t_circle:
                return [dis, self.color.unwrap(), self.pos.unwrap(), self.size / 2]
            elif self.type == self.t_square:
                return [dis, self.color.unwrap(), (self.pos - self.size / 2).unwrap() + (self.size * 2).unwrap()]
        else:
            quit(f"Library {out_library.lower()} is not supported by Morztypes! Right now the only supproted library is pygame.")