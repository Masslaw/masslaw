import unittest
from unittest.mock import patch

import numpy as np

from shared_layer.memory_utils.controlled_data_loading.builtin_loaders import MemoryControlledOpenCVImageLoader


class TestClassMemoryControlledOpenCVImageLoader(unittest.TestCase):

    def setUp(self):
        self.loader = MemoryControlledOpenCVImageLoader()

    @patch('cv2.imread')
    def test_function_load_data(self, mock_imread):
        dummy_image = np.array([[1, 2], [3, 4]])
        mock_imread.return_value = dummy_image
        input_path = "dummy_image_path.jpg"
        result = self.loader.load_data(input_path)
        mock_imread.assert_called_once_with(input_path)
        self.assertTrue((result == dummy_image).all())
