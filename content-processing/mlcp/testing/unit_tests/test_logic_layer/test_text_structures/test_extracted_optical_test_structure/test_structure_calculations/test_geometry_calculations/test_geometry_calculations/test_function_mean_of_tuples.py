import unittest
import numpy as np

from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import mean_of_tuples


class TestFunctionMeanOfTuples(unittest.TestCase):

    def test_valid_input(self):
        tuples = [(5.0, 10.0), (15.0, 20.0)]
        result = mean_of_tuples(tuples)
        self.assertEqual(result, (10.0, 15.0))

    def test_empty_input(self):
        tuples = []
        result = mean_of_tuples(tuples)
        self.assertEqual(result, (0.0, 0.0))

    def test_unequal_tuple_sizes(self):
        tuples = [(10.0, 20.0, 30.0), (10.0, 20.0)]
        with self.assertRaises(ValueError):
            mean_of_tuples(tuples)
