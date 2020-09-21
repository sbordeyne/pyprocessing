from unittest import TestCase
from copy import copy

from pyprocessing.math import PVector


class PyProcessingMathTest(TestCase):
    def setUp(self):
        pass

    def test_pvector_instanciation(self):
        '''
        Test instanciating a vector
        '''
        vector = PVector(0, 0, 0)
        self.assertIsInstance(vector, PVector)

    def test_pvector_addition(self):
        '''
        Test additioning one vector to another
        '''
        vector = PVector(0, 1, 0)
        adder = PVector(1, 0, 0)
        self.assertEqual(PVector(1, 1, 0), vector + adder)
        self.assertEqual(PVector(1, 1, 0), vector.add(adder))
        self.assertEqual(PVector(1, 1, 0), PVector.add(vector, adder))
        self.assertEqual(PVector(1, 1, 0), vector.add((1, 0, 0)))
        self.assertEqual(PVector(1, 1, 0), vector.add(1, 0, 0))

    def test_pvector_difference(self):
        '''
        Test substracting one vector to another
        '''
        vector = PVector(1, 0, 0)
        diff = PVector(1, 0, 0)
        self.assertEqual(PVector(0, 0, 0), vector - diff)
        self.assertEqual(PVector(0, 0, 0), vector.sub(diff))
        self.assertEqual(PVector(0, 0, 0), PVector.sub(vector, diff))
        self.assertEqual(PVector(0, 0, 0), vector.sub((1, 0, 0)))
        self.assertEqual(PVector(0, 0, 0), vector.sub(1, 0, 0))

    def test_pvector_mult(self):
        '''
        Test multiplying by a scalar, computing the cross product, and the dot
        product.
        '''
        self.assertEqual(PVector(2, 2, 2), PVector(1, 1, 1) * 2)
        self.assertEqual(PVector(2, 2, 2), PVector(1, 1, 1).mult(2))
        self.assertEqual(6, PVector(1, 1, 1) * PVector(2, 2, 2))
        self.assertEqual(6, PVector(1, 1, 1) * (2, 2, 2))
        self.assertEqual(6, PVector(1, 1, 1) * [2, 2, 2])
        self.assertEqual(PVector(0, 0, 0), PVector(1, 1, 1) @ PVector(2, 2, 2))
        self.assertEqual(PVector(1, 0, 0), PVector(0, 0, 1) @ PVector(0, -1, 0))
        self.assertEqual(PVector(0, 0, 0), PVector(1, 1, 1).cross(PVector(2, 2, 2)))
        self.assertEqual(PVector(1, 0, 0), PVector(0, 0, 1).cross(PVector(0, -1, 0)))

    def test_pvector_div(self):
        '''
        Test dividing a vector by a scalar
        '''
        self.assertEqual(PVector(1, 1, 1), PVector(2, 2, 2) / 2.)
        self.assertEqual(PVector(1, 1, 1), PVector(2, 2, 2).div(2))

    def test_pvector_copy(self):
        '''
        Test that copying a vector returns a new instance
        '''
        vec = PVector(0, 0, 0)
        cp = copy(vec)
        cp2 = vec.copy()

        self.assertEqual(vec, cp)
        self.assertEqual(vec, cp2)
        self.assertIsNot(vec, cp)
        self.assertIsNot(vec, cp2)

    def test_pvector_lerp(self):
        '''
        Test that linear interpolation of a vector to another returns the proper
        value
        '''
        vec = PVector(0, 0, 0)
        target = PVector(2, 2, 2)
        self.assertEqual(PVector(1, 1, 1), vec.lerp(target, 0.5))
        self.assertIs(vec, vec.lerp(target, 0))
        self.assertIs(target, vec.lerp(target, 1))

    def test_pvector_shorthands(self):
        '''
        Test that PVector shorthands for common vectors work properly
        '''
        self.assertEqual(PVector(0, 0, 0), PVector.zero)
        self.assertEqual(PVector(1, 1, 1), PVector.one)
        self.assertEqual(PVector(1, 0, 0), PVector.x_unit)
        self.assertEqual(PVector(0, 1, 0), PVector.y_unit)
        self.assertEqual(PVector(0, 0, 1), PVector.z_unit)

    def test_pvector_swizzle(self):
        '''
        Test that swizzle operations to scramble vector elements behave as expected
        '''
        vec = PVector(1, 2, 3, 4)

        self.assertEqual(PVector(1, 1, 1), vec.xxx)
        self.assertEqual(PVector(2, 2, 2), vec.yyy)
        self.assertEqual(PVector(3, 2, 1), vec.zyx)
        self.assertEqual(PVector(3, 2, 1, 4), vec.zyxw)
        self.assertEqual(1, vec.x)
        self.assertEqual(2, vec.y)
        self.assertEqual(3, vec.z)
        self.assertEqual(4, vec.w)
        vec.xyz = 2, 4, 6
        self.assertEqual(PVector(2, 4, 6, 4), vec)
        vec.zxw = 1, 2, 4
        self.assertEqual(PVector(2, 4, 1, 4), vec)

    def test_pvector_normalization(self):
        '''
        Test that normalization operations work properly
        '''
        vec = PVector(1, 2, 3)
        self.assertEqual(vec.dot(vec), vec.mag_sq())
        self.assertAlmostEqual(vec.normalized().mag(), 1)
        vec.normalize()
        self.assertAlmostEqual(vec.mag_sq(), 1)
