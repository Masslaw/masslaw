import os
import shutil
import tempfile
import unittest

import numpy as np

from shared_layer.memory_utils.storage_cached_image import StorageCachedImage


class TestClassStorageCachedImage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sample_image = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]], [[255, 0, 0], [0, 255, 0], [0, 0, 255]], [[255, 0, 0], [0, 255, 0], [0, 0, 255]]])

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_set_image(self):
        image_cache = StorageCachedImage()

        image_cache.set_image(self.sample_image)

        self.assertTrue(os.path.exists(image_cache.get_dir()))

    def test_get_image(self):
        image_cache = StorageCachedImage()
        image_cache.set_image(self.sample_image)

        result_image = image_cache.get_image()

        self.assertTrue(np.array_equal(result_image, self.sample_image))

    def test_duplicate(self):
        image_cache = StorageCachedImage()
        image_cache.set_image(self.sample_image)

        duplicate_image_cache = image_cache.duplicate()
        duplicate_image = duplicate_image_cache.get_image()

        self.assertTrue(np.array_equal(duplicate_image, self.sample_image))
        self.assertNotEqual(image_cache.get_dir(), duplicate_image_cache.get_dir())

    def test_save_to(self):
        image_cache = StorageCachedImage()
        image_cache.set_image(self.sample_image)

        save_path = os.path.join(self.temp_dir, "test_save.png")
        image_cache.save_to(save_path)

        self.assertTrue(os.path.exists(save_path))
