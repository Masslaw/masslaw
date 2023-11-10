import unittest

from shared_layer.file_system_utils._file_system_utils import get_human_readable_size


class TestFunctionGetHumanReadableSize(unittest.TestCase):

    def test_bytes(self):
        self.assertEqual(get_human_readable_size(500), "500.00 bytes")

    def test_kilobytes(self):
        self.assertEqual(get_human_readable_size(1024), "1.00 KB")
        self.assertEqual(get_human_readable_size(1500), "1.46 KB")

    def test_megabytes(self):
        self.assertEqual(get_human_readable_size(1024 * 1024), "1.00 MB")
        self.assertEqual(get_human_readable_size(1024 * 1500), "1.46 MB")

    def test_gigabytes(self):
        self.assertEqual(get_human_readable_size(1024 * 1024 * 1024), "1.00 GB")
        self.assertEqual(get_human_readable_size(1024 * 1024 * 1500), "1.46 GB")

    def test_terabytes(self):
        self.assertEqual(get_human_readable_size(1024 * 1024 * 1024 * 1024), "1.00 TB")
        self.assertEqual(get_human_readable_size(1024 * 1024 * 1024 * 1500), "1.46 TB")
