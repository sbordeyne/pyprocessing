from collections.abc import Iterable
import math
import random
import re


__all__ = ('PVector', )
SWIZZLE_RE = re.compile('^[xyzwrgba]+$')
SWIZZLE_ORDER = {
    'x': 0,
    'y': 1,
    'z': 2,
    'w': 3,
    'r': 0,
    'g': 1,
    'b': 2,
    'a': 3
}


class PVectorMeta(type):
    def __getattr__(self, attr):
        if attr == 'add':
            return self._class_add
        if attr == 'dist':
            return self._class_dist
        if attr == 'sub':
            return self._class_sub
        if attr == 'zero':
            return self._class_zero()
        if attr == 'one':
            return self._class_one()
        if attr == 'x_unit':
            return self._class_x()
        if attr == 'y_unit':
            return self._class_y()
        if attr == 'z_unit':
            return self._class_z()

        raise AttributeError(f'PVector does not contain attribute {attr}')

    @staticmethod
    def _class_add(vec1, vec2):
        return vec1 + vec2

    @staticmethod
    def _class_sub(vec1, vec2):
        return vec1 - vec2

    @staticmethod
    def _class_dist(vec1, vec2):
        return vec1.dist(vec2)

    @staticmethod
    def _class_zero():
        return PVector(0, 0, 0)

    @staticmethod
    def _class_one():
        return PVector(1, 1, 1)

    @staticmethod
    def _class_x():
        return PVector(1, 0, 0)

    @staticmethod
    def _class_y():
        return PVector(0, 1, 0)

    @staticmethod
    def _class_z():
        return PVector(0, 0, 1)


class PVector(metaclass=PVectorMeta):
    @classmethod
    def random_n(cls, n):
        return cls(*(random.random() - 0.5 for _ in range(n))).normalized()

    @classmethod
    def random_2d(cls):
        return cls.random_n(2)

    @classmethod
    def random_3d(cls):
        return cls.random_n(3)

    # generic swizzling methods
    def __swizzle_get(self, components):
        try:
            if len(components) == 1:
                return self[SWIZZLE_ORDER[components]]

            return PVector(*(self[SWIZZLE_ORDER[letter]] for letter in components))

        except IndexError:
            raise AttributeError(components)

    def __swizzle_set(self, components, values):
        if isinstance(values, (float, int)):
            values = (values,) * len(components)

        elif isinstance(values, complex):
            values = (values.real, values.imag)

        if not len(components) == len(values):
            raise ValueError('sequence is not of the same size as the swizzle')

        new_seq = self.seq.copy()

        for letter, v in zip(components, values):
            index = SWIZZLE_ORDER[letter]
            if index >= len(self):
                raise AttributeError(components)

            new_seq[index] = v

        self.seq = new_seq

    def __getattr__(self, attr):
        if SWIZZLE_RE.match(attr):
            return self.__swizzle_get(attr)

        if attr == 'add':
            return self._instance_add

        if attr == 'sub':
            return self._instance_sub

        if attr == 'dist':
            return self._instance_dist

        raise AttributeError(f'PVector does not contain attribute {attr}')

    def __setattr__(self, attr, val):
        if SWIZZLE_RE.match(attr):
            return self.__swizzle_set(attr, val)

        return super().__setattr__(attr, val)

    def _instance_add(self, *vector, x=0, y=0, z=0):
        if len(vector) == 0:
            vector = (x, y, z)

        elif isinstance(vector[0], (list, tuple, PVector)):
            vector = vector[0]

        return self + vector

    def _instance_sub(self, *vector, x=0, y=0, z=0):
        if len(vector) == 0:
            vector = (x, y, z)

        elif isinstance(vector[0], (list, tuple, PVector)):
            vector = vector[0]

        return self - vector

    def _instance_dist(self, v2):
        return (self - v2).mag()

    def mult(self, scalar=1):
        return self * scalar

    def div(self, scalar=1):
        return self / scalar

    def set_mag(self, mag, target=None):
        if target is None:
            target = self
        target.normalize()
        for i in range(len(target)):
            target[i] *= mag

    @staticmethod
    def from_angle(angle, target=None):
        x = math.cos(angle)
        y = math.sin(angle)
        if target is None:
            return PVector(x, y)
        target.set(x, y)
        return target

    def __init__(self, *args, x=0, y=0, z=None):
        if isinstance(args[0], complex):
            self.seq = [args[0].real, args[0].imag]
            return

        if args:
            self.seq = list(args)
            return

        self.seq = [x, y, z] if z is not None else [x, y]

    def __copy__(self):
        return self.copy()

    def __add__(self, other):
        if isinstance(other, complex):
            other = (other.real, other.imag)

        if isinstance(other, Iterable):
            return PVector(*(cmpnt_a + cmpnt_b for cmpnt_a, cmpnt_b in zip(self, other)))

        raise TypeError(
            f"Invalid operand '+' for type PVector and {type(other)}"
        )

    def __sub__(self, other):
        if isinstance(other, complex):
            other = (other.real, other.imag)

        if isinstance(other, Iterable):
            return PVector(*(cmpnt_a - cmpnt_b for cmpnt_a, cmpnt_b in zip(self, other)))

        raise TypeError(
            f"Invalid operand '-' for type PVector and {type(other)}"
        )

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return PVector(*(cmpnt_a * other for cmpnt_a in self))

        if isinstance(other, Iterable):
            return self.dot(other)

        raise TypeError(
            f"Invalid operand '*' for type PVector and {type(other)}"
        )

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return PVector(*(cmpnt_a / other for cmpnt_a in self))

        raise TypeError(
            f"Invalid operand '/' for type PVector and {type(other)}"
        )

    def __floordiv__(self, other):
        if isinstance(other, (float, int)):
            return PVector(*(cmpnt_a // other for cmpnt_a in self))

        raise TypeError(
            f"Invalid operand '//' for type PVector and {type(other)}"
        )

    def __matmul__(self, other):
        if isinstance(other, Iterable):
            return self.cross(other)

    def __str__(self):
        return ' '.join(str(i) for i in self)

    def __repr__(self):
        return f"PVector<{', '.join(str(i) for i in self)}> at {id(self)}"

    def __len__(self):
        return len(self.seq)

    def __iter__(self):
        return iter(self.seq)

    def __eq__(self, other):
        if not isinstance(other, Iterable):
            return False

        if not len(other) == len(self):
            return False

        if not all(cmpnt_a == cmpnt_b for cmpnt_a, cmpnt_b in zip(self, other)):
            return False

        return True

    def __getitem__(self, item):
        if isinstance(item, str) and SWIZZLE_RE.match(item):
            return self.__swizzle_get(item)

        if isinstance(item, int):
            return self.seq[item]

        raise KeyError(f"Item '{item}' cannot be accessed.")

    def __setitem__(self, item, v):
        if isinstance(item, str) and SWIZZLE_RE.match(item):
            return self.__swizzle_get(item)

        if isinstance(item, int):
            self.seq[item] = v
            return

        raise KeyError(f"Item '{item}' cannot be accessed.")

    @property
    def position(self):
        return tuple(self)

    @property
    def is_2d(self):
        return len(self) == 2

    @property
    def is_3d(self):
        return len(self) == 3

    @property
    def is_4d(self):
        return len(self) == 4

    def set(self, *vector, x=None, y=None, z=None):
        self.seq = PVector(*vector, x, y, z).seq

    def copy(self):
        return PVector(*self)

    def mag(self):
        return math.sqrt(self.mag_sq())

    def mag_sq(self):
        return sum(cmpnt_a * cmpnt_a for cmpnt_a in self)

    def dot(self, other):
        return sum(cmpnt_a * cmpnt_b for cmpnt_a, cmpnt_b in zip(self, other))

    def cross(self, other):
        if not len(self) == 3:
            raise ValueError(
                'Cross product is only supported for 3d vectors.'
            )
        x = self[1] * other[2] - self[2] * other[1]
        y = self[2] * other[0] - self[0] * other[2]
        z = self[0] * other[1] - self[1] * other[0]
        return PVector(x, y, z)

    def normalize(self):
        mag = self.mag()
        if mag == 0:
            return
        for i in range(len(self)):
            self[i] /= mag

    def normalized(self):
        v = self.copy()
        v.normalize()
        return v

    def limit(self, limit):
        magsq = self.mag_sq()
        if magsq <= limit * limit:
            return

        magsq = math.sqrt(magsq) / limit

        for i in range(len(self)):
            self[i] /= magsq

    def heading(self):
        if not self.is_2d:
            raise ValueError('Cannot calculate heading on a 3D Vector.')
        return math.atan2(self[1], self[0])

    def rotate(self, theta):
        if not self.is_2d:
            raise ValueError(f"Can't rotate a non 2D vector")

        self[0] = math.cos(theta) * self[0] - math.sin(theta) * self[1]
        self[1] = math.sin(theta) * self[0] + math.cos(theta) * self[1]

    def rotated(self, theta):
        v = self.copy()
        v.rotate(theta)
        return v

    def lerp(self, target, amount):
        if amount == 0:
            return self
        if amount == 1:
            return target
        return target * amount + self * (1 - amount)

    def angle_between(self, other):
        return math.acos(self.dot(other) / (self.mag() * other.mag()))

    def array(self):
        return self.position

    def gen_single_component_access(letter):
        idx = SWIZZLE_ORDER[letter]

        @property
        def getter(self):
            if not len(self.seq) <= idx:
                return self.seq[idx]

            raise IndexError(f'PVector does not have {idx+1} elements')

        @getter.setter
        def setter(self, val):
            if not len(self.seq) <= idx:
                self.seq[idx] = val
                return

            raise IndexError(f'PVector does not have {idx+1} elements')

        return setter

    x = gen_single_component_access('x')
    y = gen_single_component_access('y')
    z = gen_single_component_access('z')
    w = gen_single_component_access('w')
    r = gen_single_component_access('r')
    g = gen_single_component_access('g')
    b = gen_single_component_access('b')
    a = gen_single_component_access('a')

    del gen_single_component_access
