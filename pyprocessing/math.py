import math
import random

from pyprocessing.calculation import lerp


__all__ = ('PVector', )


class PVectorMeta(type):
    def __getattr__(self, attr):
        if attr == 'add':
            return self._class_add
        if attr ==  'dist':
            return self._class_dist
        if attr == 'sub':
            return self._class_sub
        return super().__getattr__(attr)

    @staticmethod
    def _class_add(vec1, vec2):
        return vec1 + vec2

    @staticmethod
    def _class_sub(vec1, vec2):
        return vec1 - vec2

    @staticmethod
    def _class_dist(vec1, vec2):
        return vec1.dist(vec2)


class PVector(metaclass=PVectorMeta):
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

    def __getattr__(self, attr):
        if attr == 'add':
            return self._instance_add
        if attr ==  'dist':
            return self._instance_dist
        if attr == 'sub':
            return self._instance_sub
        return super().__getattr__(attr)

    def _instance_add(self, *vector, x=0, y=0, z=0):
        if vector:
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
        vec = self.copy()
        vec.x += x
        vec.y += y
        if z is not None:
            vec.z += z
        return vec

    def _instance_sub(self, *vector, x=0, y=0, z=0):
        if vector:
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
        vec = self.copy()
        vec.x -= x
        vec.y -= y
        if z is not None:
            vec.z -= z
        return vec

    def _instance_dist(self, v2):
        return math.dist(self.position, v2.position)

    def mult(self, scalar=1):
        vec = self.copy()
        vec.x *= scalar
        vec.y *= scalar
        if vec.z is not None:
            vec.z *= scalar
        return vec

    def div(self, scalar=1):
        vec = self.copy()
        vec.x /= scalar
        vec.y /= scalar
        if vec.z is not None:
            vec.z /= scalar
        return vec

    @classmethod
    def set_mag(cls, mag, target=None):
        if target is not None:
            target.normalize()
            target *= mag
            return target
        cls.normalize()
        cls *= mag
        return cls

    @staticmethod
    def from_angle(angle, target=None):
        x = math.cos(angle)
        y = math.sin(angle)
        if target is None:
            return PVector(x, y)
        target.set(x, y)
        return target

    def __init__(self, x=0, y=0, z=None):
        self.x, self.y, self._z = x, y, z
        self.is_2d = z is None

    def __copy__(self):
        return self.copy()

    def __add__(self, other):
        if isinstance(other, (list, tuple)):
            return self.add(*other)
        elif isinstance(other, (PVector, complex)):
            return self.add(other)
        raise TypeError(
            f"Invalid operand '+' for type PVector and {type(other)}"
        )

    def __sub__(self, other):
        if isinstance(other, (list, tuple)):
            return self.sub(*other)
        elif isinstance(other, (PVector, complex)):
            return self.sub(other)
        raise TypeError(
            f"Invalid operand '-' for type PVector and {type(other)}"
        )

    def __mul__(self, other):
        if isinstance(other, PVector):
            return self.dot(other)
        elif isinstance(other, (list, tuple)):
            return self.dot(PVector(*other))
        elif isinstance(other, (float, int)):
            return self.mult(other)
        raise TypeError(
            f"Invalid operand '*' for type PVector and {type(other)}"
        )

    def __div__(self, other):
        if isinstance(other, (float, int)):
            return self.div(other)
        raise TypeError(
            f"Invalid operand '/' for type PVector and {type(other)}"
        )

    def __matmul__(self, other):
        if isinstance(other, PVector):
            return self.cross(other)
        raise TypeError(
            f"Invalid operand '@' for type PVector and {type(other)}"
        )

    def __str__(self):
        if self.is_2d:
            return f'{self.x} {self.y}'
        return f'{self.x} {self.y} {self.z}'

    def __repr__(self):
        return f'PVector<{", ".join(str(self).split())}> at {id(self)}'

    def __eq__(self, other):
        if isinstance(other, PVector):
            return all(
                m1 == m2 for m1, m2 in zip(self.position, other.position)
            )
        if isinstance(other, (list, tuple)):
            return all(m1 == m2 for m1, m2 in zip(self.position, other))
        raise ValueError(
            f"Invalid operand '==' for type Pvector and {type(other)}"
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

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return PVector(x, y, z)

    def normalize(self):
        mag = self.mag()
        self.x /= mag
        self.y /= mag
        self.z /= mag

    def limit(self, limit):
        if self.mag_sq() <= limit ** 2:
            return

        self.normalize()
        self *= limit

    def heading(self):
        if not self.is_2d:
            raise ValueError('Cannot calculate heading on a 3D Vector.')
        return math.atan2(self.y, self.x)

    def rotate(self, theta):
        if not self.is_2d:
            raise ValueError('Cannot rotate a 3D Vector.')
        self.x = math.cos(theta) * self.x - math.sin(theta) * self.y
        self.y = math.sin(theta) * self.x + math.cos(theta) * self.y

    def lerp(self, target, amount):
        if not (0 <= amount <= 1):
            raise ValueError('`amount` must be between 0 and 1.')
        if float(amount) == 0.0:
            return self
        if float(amount) == 1.0:
            return target
        x = lerp(self.x, target.x, amount)
        y = lerp(self.y, target.y, amount)
        z = lerp(self.z, target.z, amount)
        if self.is_2d and target.is_2d:
            z = None
        return PVector(x, y, z)

    def angle_between(self, other):
        return math.acos(self.dot(other) / (self.mag() * other.mag()))

    def array(self):
        return self.position
