import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_merging._sequential_merging._continuity_check_functions import line_continuity_check_function


class TestFunctionLineContinuityCheckFunction(unittest.TestCase):
    def test_continuous(self):
        line1 = OpticalTextStructureLine()
        line1.set_children(list('Hello'))
        line1.set_bounding_rect((0, 0, 50, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children(list('There'))
        line2.set_bounding_rect((45, 0, 95, 10))

        self.assertTrue(line_continuity_check_function(line1, line2))

    def test_not_continuous_for_large_gap(self):
        line1 = OpticalTextStructureLine()
        line1.set_children(list('Hello'))
        line1.set_bounding_rect((0, 0, 50, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children(list('There'))
        line2.set_bounding_rect((100, 0, 150, 10))

        self.assertFalse(line_continuity_check_function(line1, line2))

    def test_not_continuous_for_character_size_diff(self):
        line1 = OpticalTextStructureLine()
        line1.set_children(list('Hello'))
        line1.set_bounding_rect((0, 0, 50, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children(list('There'))
        line2.set_bounding_rect((50, 0, 150, 10))

        self.assertFalse(line_continuity_check_function(line1, line2))

    def test_not_continuous_for_height_diff(self):
        line1 = OpticalTextStructureLine()
        line1.set_children(list('Hello'))
        line1.set_bounding_rect((0, 0, 50, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children(list('There'))
        line2.set_bounding_rect((50, 0, 100, 20))

        self.assertFalse(line_continuity_check_function(line1, line2))

    def test_not_continuous_for_offset(self):
        line1 = OpticalTextStructureLine()
        line1.set_children(list('Hello'))
        line1.set_bounding_rect((0, 0, 50, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children(list('There'))
        line2.set_bounding_rect((50, 5, 100, 15))

        self.assertFalse(line_continuity_check_function(line1, line2))
