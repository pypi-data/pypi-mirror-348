import unittest
from matholib import math_add


class TestMatholib(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(math_add([1, 2, 3]), 6)

    def test_add_empty_list(self):
        self.assertEqual(math_add([]), 0)

    def test_add_invalid_input(self):
        with self.assertRaises(TypeError):
            math_add('123')
