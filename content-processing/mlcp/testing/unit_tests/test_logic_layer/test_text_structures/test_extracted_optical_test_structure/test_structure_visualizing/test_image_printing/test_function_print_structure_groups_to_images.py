import unittest
from unittest.mock import patch

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._exceptions import InvalidNumberOfPrintTargetImages
from logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._image_printing import print_structure_children_to_images


class TestFunctionPrintStructureGroupsToImages(unittest.TestCase):
    def setUp(self):
        self.document = ExtractedOpticalTextDocument()
        self.word1 = OpticalTextStructureWord()
        self.word1.set_children(list('hello'))
        self.word1.set_bounding_rect((5, 5, 10, 10))
        self.word2 = OpticalTextStructureWord()
        self.word2.set_children(list('world'))
        self.word2.set_bounding_rect((20, 5, 20, 20))
        self.document.get_structure_root().set_children([self.word1, self.word2])

        self.cv2_patcher = patch('logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._image_printing.cv2')
        self.cv2_mock = self.cv2_patcher.start()

    def tearDown(self):
        self.cv2_patcher.stop()

    def test_printing_correct_rectangles(self):
        self.cv2_mock.imread.side_effect = [[1, 0], [0, 1]]

        print_structure_children_to_images(self.document.get_structure_root(), ['image1', 'image2'], line_thickness=2)

        self.cv2_mock.rectangle.assert_any_call([1, 0], (5, 5), (10, 10), (255, 0, 0), 2)
        self.cv2_mock.rectangle.assert_any_call([0, 1], (20, 5), (20, 20), (255, 0, 0), 2)

    def test_real_image_assertion(self):
        self.cv2_mock.imread.return_value = None
        with self.assertRaises(ValueError):
            print_structure_children_to_images(self.document.get_structure_root(), ['image1', 'image2'])
        self.cv2_mock.imread.return_value = [1, 0]
        print_structure_children_to_images(self.document.get_structure_root(), ['image1', 'image2'])

    def test_image_number_assertion(self):
        with self.assertRaises(InvalidNumberOfPrintTargetImages):
            print_structure_children_to_images(self.document.get_structure_root(), ['image1'])
        with self.assertRaises(InvalidNumberOfPrintTargetImages):
            print_structure_children_to_images(self.document.get_structure_root(), ['image1', 'image2', 'image3'])
        print_structure_children_to_images(self.document.get_structure_root(), ['image1', 'image2'])
