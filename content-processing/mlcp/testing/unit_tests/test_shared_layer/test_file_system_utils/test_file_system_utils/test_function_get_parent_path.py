import unittest

from shared_layer.file_system_utils._file_system_utils import get_parent_path


class TestFunctionGetParentPath(unittest.TestCase):

    def test_valid_path_and_folder(self):
        path = "/user/home/documents/music/rock"
        folder = "documents"
        result = get_parent_path(path, folder)
        expected = "/user/home"
        self.assertEqual(result, expected)

    def test_invalid_folder(self):
        path = "/user/home/documents/music/rock"
        folder = "downloads"
        with self.assertRaises(ValueError) as context:
            get_parent_path(path, folder)
        self.assertTrue("Folder 'downloads' not found in path" in str(context.exception))

    def test_folder_at_end(self):
        path = "/user/home/documents"
        folder = "documents"
        result = get_parent_path(path, folder)
        expected = "/user/home"
        self.assertEqual(result, expected)

    def test_folder_at_start(self):
        path = "/user/home/documents/music/rock"
        folder = "user"
        result = get_parent_path(path, folder)
        expected = "/"
        self.assertEqual(result, expected)
