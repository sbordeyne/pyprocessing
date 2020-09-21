from unittest import TestCase

from pyprocessing.math import PVector


class PyProcessingMathTest(TestCase):
    def setUp(self):
        pass

    def test_pvector_instanciation(self):
        vector = PVector(0, 0, 0)
        self.assertIsInstance(vector, PVector)

    def test_pvector_addition(self):
        vector = PVector(0, 1, 0)
        adder = PVector(1, 0, 0)
        self.assertEqual(PVector(1, 1, 0), vector + adder)
        self.assertEqual(PVector(1, 1, 0), vector.add(adder))
        self.assertEqual(PVector(1, 1, 0), PVector.add(vector, adder))
        self.assertEqual(PVector(1, 1, 0), vector.add((1, 0, 0)))
        self.assertEqual(PVector(1, 1, 0), vector.add(1, 0, 0))

    def test_pvector_difference(self):
        vector = PVector(1, 0, 0)
        diff = PVector(1, 0, 0)
        self.assertEqual(PVector(0, 0, 0), vector - diff)
        self.assertEqual(PVector(0, 0, 0), vector.sub(diff))
        self.assertEqual(PVector(0, 0, 0), PVector.sub(vector, diff))
        self.assertEqual(PVector(0, 0, 0), vector.sub((1, 0, 0)))
        self.assertEqual(PVector(0, 0, 0), vector.sub(1, 0, 0))
