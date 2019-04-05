import unittest
from calculator import mul

class CalculatorTestCase(unittest.TestCase):
    def test_mul(self):
        self.assertEqual(mul(2, 2), 4)
    def test_mul2(self):
       self.assertEqual(mul(2, 3), 6)
