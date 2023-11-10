import unittest
from unittest.mock import patch

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._image_printing import print_structure_element_to_image


class TestFunctionPrintStructureElementToImage(unittest.TestCase):
    def setUp(self):
        self.cv2_patcher = patch('logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._image_printing.cv2')
        self.cv2_mock = self.cv2_patcher.start()

    def tearDown(self):
        self.cv2_patcher.stop()

    def test_printing_correct_rectangles(self):
        self.cv2_mock.imread.side_effect = [[1, 0], [0, 1]]

        bounding_rectangle = (0, 10, 20, 30)
        word_element = OpticalTextStructureWord()
        word_element.set_children(list('hello'))
        word_element.set_bounding_rect(bounding_rectangle)
        image_data = [1, 0]
        print_structure_element_to_image(word_element, image_data, line_thickness=2)

        self.cv2_mock.rectangle.assert_called_once_with(image_data, (bounding_rectangle[0], bounding_rectangle[1]), (bounding_rectangle[2], bounding_rectangle[3]), (255, 0, 0), 2)

    def test_real_image_assertion(self):
        word_element = OpticalTextStructureWord()
        word_element.set_children(list('hello'))
        word_element.set_bounding_rect((0, 10, 20, 30))
        with self.assertRaises(ValueError):
            print_structure_element_to_image(word_element, None)
        print_structure_element_to_image(word_element, [1, 0])
