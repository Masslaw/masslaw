import unittest
from unittest.mock import patch

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._structure_visualizer import StructureVisualizer


class TestClassStructureVisualizer(unittest.TestCase):

    def setUp(self):
        self.document = ExtractedOpticalTextDocument()
        word1 = OpticalTextStructureWord()
        word1.set_children(list('hello'))
        word1.set_bounding_rect((5, 5, 10, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('world'))
        word2.set_bounding_rect((20, 5, 20, 20))
        self.document.get_structure_root().set_children([word1, word2])

        self.cv2_patcher = patch('logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._image_printing.cv2')
        self.cv2_mock = self.cv2_patcher.start()

        self.structure_visualizer = StructureVisualizer(self.document)

    def tearDown(self):
        self.cv2_patcher.stop()

    def test_printing_correct_rectangles(self):
        self.structure_visualizer.print_group_visualizations_to_images(['image1', 'image2'], line_thickness=2)

        self.cv2_mock.rectangle.assert_any_call(self.cv2_mock.imread.return_value, (5, 5), (10, 10), (255, 0, 0), 2)
        self.cv2_mock.rectangle.assert_any_call(self.cv2_mock.imread.return_value, (20, 5), (20, 20), (255, 0, 0), 2)
