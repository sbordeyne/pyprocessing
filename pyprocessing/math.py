import math
import random


class PVector:
    @classmethod
    def random_2d(cls):
        vector = PVector(random.random(), random.random())
        vector.normalize()
        return vector

    @classmethod
    def random_3d(cls):
        vector = PVector(random.random(), random.random(), random.random())
        vector.normalize()
        return vector

    @classmethod
    def add(cls, *vector, x=0, y=0, z=0):
        if vector:
            if all(isinstance(v, PVector) for v in vector):
                vec = PVector(*vector[0])
                vec.add(vector[1])
                return vec
            if isinstance(vector[0], PVector):
                x, y, z = vector[0].position
            elif isinstance(vector[0], (list, tuple)):
                x, y, *_ = vector[0]
                if len(vector[0]) == 3:
                    z = vector[0][2]
                else:
                    z = None
            elif all(isinstance(p, (int, float)) for p in vector):
                x, y, z = vector
            elif isinstance(vector[0], complex):
                x, y, z = vector[0].real, vector[0].imag, None
        cls.x += x
        cls.y += y
        if z is not None:
            cls.z += z
        return cls

    @staticmethod
    def from_angle(angle, target=None):
        x = math.cos(angle)
        y = math.sin(angle)
        if target is None:
            return PVector(x, y)
        target.set(x, y)
        return target

    def __init__(self, x, y, z=None):
        self.x, self.y, self._z = x, y, z
        self.is_2d = z is None

    def __copy__(self):
        return self.copy()

    def __add__(self, other):
        if isinstance(other, (list, tuple)):
            return self.add(*other)
        elif isinstance(other, (PVector, complex)):
            return self.add(other)
        else:
            raise TypeError(
                f"Invalid operand '+' for type PVector and {type(other)}"
            )

    @property
    def z(self):
        if self._z is None:
            return 0
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        if value is not None:
            self.is_2d = False

    @property
    def position(self):
        return self.x, self.y, self.z

    def set(self, *vector, x=None, y=None, z=None):
        if vector:
            if isinstance(vector[0], PVector):
                self.x, self.y, self.z = vector[0].position
            elif isinstance(vector[0], (list, tuple)):
                self.x, self.y, *_ = vector[0]
                if len(vector[0]) == 3:
                    self.z = vector[0][2]
                else:
                    self.z = None
            elif all(isinstance(p, (int, float)) for p in vector):
                self.x, self.y, self.z = vector
            elif isinstance(vector[0], complex):
                self.x, self.y, self.z = vector[0].real, vector[0].imag, None
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z

    def copy(self):
        return PVector(self.x, self.y, self._z)

    def mag(self):
        return math.sqrt(self.mag_sq())

    def mag_sq(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self):
        mag = self.mag()
        self.x /= mag
        self.y /= mag
        self.z /= mag